from model.enums.EtapaProcessamentoEnum import EtapaProcessamentoEnum
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum
from service.AmenidadeMunicipioService import AmenidadeMunicipioService
from service.HistoricoErroService import HistoricoErroService
from service.MunicipioService import MunicipioService
from service.client.OSMNXClientService import OSMNXClientService
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from datetime import datetime
from pandas import DataFrame, Series
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class ExtracaoAmenidadesComponent:

    amenidade_municipio_service = AmenidadeMunicipioService()
    historico_erro_service = HistoricoErroService()
    municipio_service = MunicipioService()
    osmxn_client_service = OSMNXClientService()

    def verificar_nao_existencia_registros_pendentes(self, conexao_bd: Connection) -> bool:
        df_qtde_registros_pendentes = self.municipio_service.buscar_qtde_registros_pendentes_extracao_amenidades(conexao_bd)
        qtde_registros_pendentes = df_qtde_registros_pendentes["quantidade"][0]

        log.info(msg=f"Há um total de {qtde_registros_pendentes} municípios a serem processados.")

        return qtde_registros_pendentes == 0
    
    def converter_tags_para_dict(self, tag: str) -> dict:
        chave = tag[:tag.index("=")]
        valor = tag[tag.index("=") + 1:]

        return {chave: valor}

    def __extrair_amenidades_municipio(self, sr_municipio: Series, df_tags_osm: DataFrame) -> tuple[DataFrame, DataFrame]:
        codigo_municipio = sr_municipio["codigo"]
        nome_municipio = sr_municipio["nome"]

        df_amenidade_municipio = DataFrame(data=[], columns=["geometria", "codigo_feicao_osm", "codigo_municipio"])
        df_historico_erro = DataFrame(data=[], columns=["entidade_erro", "chave_entidade", "etapa_erro", "mensagem_erro", "data_hora_ocorrencia"])

        try:
            log.info(msg=f"Extraindo as amenidades do município {codigo_municipio} - {nome_municipio}.")
            
            for _, sr_tag_osm in df_tags_osm.iterrows():
                tag_dict = sr_tag_osm["tag_osm"]
                gdf_feicao_osmnx = self.osmxn_client_service.obter_feicoes_por_poligono(poligono=sr_municipio["geometria"], tag=tag_dict)

                if gdf_feicao_osmnx.empty:
                    log.warning(msg=f"Nenhuma amenidade foi encontrada para o município {codigo_municipio} - {nome_municipio} utilizando a tag {tag_dict}.")
                    continue

                for _, sr_feicao in gdf_feicao_osmnx.iterrows():
                    df_amenidade_municipio.loc[len(df_amenidade_municipio)] = [
                        sr_feicao["geometry"].centroid,
                        sr_tag_osm["codigo"],
                        codigo_municipio
                    ]

            if df_amenidade_municipio.empty:
                raise Exception(f"Nenhuma amenidade foi encontrada para o município")

            log.info(msg=f"As amenidades foram extraídas com sucesso para  o município {codigo_municipio} - {nome_municipio}.")
            return df_amenidade_municipio, df_historico_erro
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao extrair as amenidades do município {codigo_municipio} - {nome_municipio}. {ExceptionUtil.montar_exception_padrao(e)}")

            df_historico_erro.loc[len(df_historico_erro)] = [
                "t_municipio",
                codigo_municipio,
                EtapaProcessamentoEnum.EXTRACAO_AMENIDADES.value,
                ExceptionUtil.montar_exception_historico_erro(e),
                datetime.now()
            ]

            return DataFrame(), df_historico_erro
        
    def processar_particao_dask(self, df_municipio: DataFrame, df_tags_osm: DataFrame) -> DataFrame:
        df_resultado = DataFrame(data=[], columns=["codigo_municipio", "dict_amenidade_municipio", "dict_historico_erro", "status"])

        for _, sr_municipio in df_municipio.iterrows():
            df_amenidade_municipio, df_historico_erro = self.__extrair_amenidades_municipio(sr_municipio, df_tags_osm)

            df_resultado.loc[len(df_resultado)] = [
                sr_municipio["codigo"],
                df_amenidade_municipio.to_dict(),
                df_historico_erro.to_dict(),
                StatusEtapaProcessamentoEnum.ERRO.value if df_amenidade_municipio.empty else StatusEtapaProcessamentoEnum.CONCLUIDO.value
            ]

        return df_resultado.set_index(keys="codigo_municipio")
    
    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            for indice, sr_resultado in df_resultado.iterrows():
                if sr_resultado["dict_amenidade_municipio"] != {}:
                    gdf_amenidade_municipio = DataFrameUtil.dict_para_geodataframe(dict_dados=sr_resultado["dict_amenidade_municipio"])
                    self.amenidade_municipio_service.salvar_geodataframe(gdf=gdf_amenidade_municipio, conexao_bd=conexao_bd)

                if sr_resultado["dict_historico_erro"] != {}:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=sr_resultado["dict_historico_erro"])
                    self.historico_erro_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": sr_resultado["status"],
                    "codigo_municipio": indice
                }

                self.municipio_service.atualizar_flag_extracao_amenidades(conexao_bd, parametros)
                log.info(msg="Os dados foram persistidos com sucesso.")
                
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e


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
from numpy import ndarray, array
from pandas import DataFrame
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
    


    def __converter_tag_para_dict(self, tag: str) -> str:
        chave = tag[:tag.index("=")]
        valor = tag[tag.index("=") + 1:]

        return {chave: valor}



    def ajustar_coluna_tag_osm(self, df_tags_osm: DataFrame) -> ndarray:
        return array(self.__converter_tag_para_dict(tag) for tag in df_tags_osm["tag_osm"].to_numpy())



    def __extrair_amenidades_municipio(self, municipio: list, df_tags_osm: DataFrame) -> tuple[list[dict], list[dict]]:
        lista_dict_amenidade_municipio = list()
        lista_dict_historico_erro = list()

        try:
            log.info(msg=f"Extraindo as amenidades do município {municipio[0]} - {municipio[1]}.")
            
            for tag_osm in df_tags_osm.to_numpy():
                gdf_feicao_osmnx = self.osmxn_client_service.obter_feicoes_por_poligono(poligono=municipio[2], tag=tag_osm[1])

                if gdf_feicao_osmnx.empty:
                    log.warning(msg=f"Nenhuma amenidade foi encontrada para o município {municipio[0]} - {municipio[1]} utilizando a tag {tag_osm[1]}.")
                    continue

                for geometria_feicao in gdf_feicao_osmnx["geometry"].to_numpy():
                    lista_dict_amenidade_municipio.append({
                        "geometria": geometria_feicao.centroid, 
                        "codigo_feicao_osm": tag_osm[0], 
                        "codigo_municipio": municipio[0]
                    })

            if not lista_dict_amenidade_municipio:
                raise Exception(f"Nenhuma amenidade foi encontrada para o município")

            log.info(msg=f"As amenidades foram extraídas com sucesso para o município {municipio[0]} - {municipio[1]}.")

            return lista_dict_amenidade_municipio, lista_dict_historico_erro
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao extrair as amenidades do município {municipio[0]} - {municipio[1]}. {ExceptionUtil.montar_erro_exception_padrao(e)}")

            lista_dict_historico_erro.append({
                "entidade_erro": "t_municipio", 
                "chave_entidade": municipio[0], 
                "etapa_erro": EtapaProcessamentoEnum.EXTRACAO_AMENIDADES.value, 
                "mensagem_erro": ExceptionUtil.montar_erro_exception_historico_erro(e), 
                "data_hora_ocorrencia": datetime.now()
            })

            return list(), lista_dict_historico_erro



    def processar_particao_dask(self, df_municipio: DataFrame, df_tags_osm: DataFrame) -> DataFrame:
        lista_dict_resultado = list()

        for municipio in df_municipio.to_numpy():
            lista_dict_amenidade_municipio, lista_dict_historico_erro = self.__extrair_amenidades_municipio(municipio, df_tags_osm)

            lista_dict_resultado.append({
                "codigo_municipio": municipio[0], 
                "lista_dict_amenidade_municipio": lista_dict_amenidade_municipio, 
                "lista_dict_historico_erro": lista_dict_historico_erro, 
                "status": StatusEtapaProcessamentoEnum.CONCLUIDO.value if lista_dict_amenidade_municipio else StatusEtapaProcessamentoEnum.ERRO.value
            })

        return DataFrame(data=lista_dict_resultado)
    


    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            log.info(msg="Persistindo os dados processados na base.")

            for resultado in df_resultado.to_numpy():
                if resultado[1]:
                    gdf_amenidade_municipio = DataFrameUtil.dict_para_geodataframe(dict_dados=resultado[1])
                    self.amenidade_municipio_service.salvar_geodataframe(gdf=gdf_amenidade_municipio, conexao_bd=conexao_bd)

                if resultado[2]:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=resultado[2])
                    self.historico_erro_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": resultado[3],
                    "codigo_municipio": resultado[0]
                }

                self.municipio_service.atualizar_flag_extracao_amenidades(conexao_bd, parametros)

            log.info(msg="Os dados foram persistidos com sucesso.")
                
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e


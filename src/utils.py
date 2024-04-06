import models

import osmnx as ox

def montar_query_osmnx(municipio:models.Municipio):
    return municipio.nome + ', ' + municipio.nome_uf + ', Brasil'

def montar_query_parametrizada(sql:str, params:dict):
    for param in params.items():
        sql = sql.replace(':' + param[0], str(param[1]))

    return sql
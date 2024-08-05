class FeicaoOSMQueriesConstantes:

    BUSCAR_TAGS_OSM_ATIVAS = '''
        SELECT 
            codigo,
            tag_osm,
            codigo_categoria_amenidade
        FROM t_feicao_osm
        WHERE flag_tag_ativa = True
        ORDER BY codigo;
    '''
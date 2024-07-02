class FeicaoOSMQueriesConstantes:

    BUSCAR_TAGS_OSM_ATIVAS = '''
        SELECT 
            codigo,
            tag_osm
        FROM t_feicao_osm
        WHERE flag_tag_ativa = True
        ORDER BY codigo;
    '''
class Columns:
    # shared columns
    year = 'ano'
    code = 'codigo_pais'
    
    # df_country
    country = 'pais'
    population = 'populacao'
    gdp = 'gdp'
    
    # df_wines & df_produced_wine
    vine_type = 'tipo_de_vinho'
    vine_category = 'categoria_do_vinho'
    vine_exported_kg = 'quantidade_de_vinho_exportada_em_kg'
    vine_produced_kg = 'quantidade_de_vinho_produzida_em_kg'
    vine_sold_usd = 'valor_vendido_em_vinho_em_usd'
    
    # df_wines & df_produced_wine
    grape = 'uva'
    grape_type = 'tipo_uva'
    grape_category = 'categoria_uva'
    grape_processed_kg = 'quantidade_de_uva_processada_em_kg'
    
    # df_weather
    preciptation = 'precipitacao_media' # mm
    preciptation_total = 'precipitacao_total' # mm
    temperature_min = 'temperatura_min' # °C
    temperature_max = 'temperatura_max' # °C
    temperature = 'temperatura_media' # °C
    humidity = 'umidade_media' # %
    
    # df_weather before processed
    date = 'data'
    hour = 'hora'
    preciptation_mm = 'precipitacao_mm'
    pression_at = 'pressao_atmosferica_mb'
    pression_at_max = 'pressao_atmosferica_max_mb'
    pression_at_min = 'pressao_atmosferica_min_mb'
    radiation_kj_m = 'radiacao_kj_m'
    temp_celcius = 'temperatura_do_ar_celcius'
    temp_orv_celcius = 'temperatura_do_ponto_de_orvalho_celcius'
    temp_max = 'temperatura_max_hora'
    temp_min = 'temperatura_min_hora'
    temp_orv_max = 'temperatura_orvalho_max_hora'
    temp_orv_min = 'temperatura_orvalho_min_hora'
    humidity_max_h = 'umidade_max_hora'
    humidity_min_h = 'umidade_min_hora'
    humidity_rel_h = 'umidade_relativa_hora'
    wind_dir = 'vento_dir'
    wind_raj = 'vento_rajada'
    wind_vel = 'vento_velocidade'
    empty_col = 'coluna_vazia'
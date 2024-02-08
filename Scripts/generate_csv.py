from utils.columns import Columns as c
from load_df_from_csv import (
    get_grapes_processed_data_df,
    get_wines_agg_df,
    get_country_agg_df,
    get_weather_data_df,
    load_and_format_exp_vinho_df,
    load_and_format_producao_vinho_df
)

def main():
    generate_requested_csv()    
    

def generate_requested_csv():
    df_exported_wine = load_and_format_exp_vinho_df()
    
    df_exported_wine['pais_origem'] = 'Brasil'
    df_exported_wine = df_exported_wine.drop([c.year,c.code], axis=1)
    
    df_agg_exported_wine = df_exported_wine.groupby(['pais_origem', c.country]).sum()
    df_agg_exported_wine = df_agg_exported_wine.reset_index()
    
    df_agg_exported_wine.to_csv(
        'Exportações de 2004 até 2019.csv',
        sep = ';',
        header=['País de origem', 'País de destino', 'Quantidade exportada em litros', 'Valor em USD'],
        index= False
    )

def generate_csv_for_all_dfs():
    df_exported_wine = load_and_format_exp_vinho_df()
    df_produced_wine = load_and_format_producao_vinho_df()
    df_grape = get_grapes_processed_data_df()
    df_wines = get_wines_agg_df()
    df_country = get_country_agg_df()
    df_weather = get_weather_data_df()
    
    df_exported_wine.to_csv('df_exported_wine.csv')
    df_produced_wine.to_csv('df_produced_wine.csv')
    df_grape.to_csv('df_grape.csv')
    df_wines.to_csv('df_wines.csv')
    df_country.to_csv('df_country.csv')
    df_weather.to_csv('df_weather.csv')


if __name__ == "__main__":
    main()

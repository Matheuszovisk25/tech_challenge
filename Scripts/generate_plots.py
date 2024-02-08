import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    df_exported_wine = load_and_format_exp_vinho_df()
    # df_produced_wine = load_and_format_producao_vinho_df()
    # df_grape = get_grapes_processed_data_df()
    # df_wines = get_wines_agg_df()
    # df_country = get_country_agg_df()
    #df_weather = get_weather_data_df()
    
    print(df_exported_wine[c.vine_exported_kg].sum())
    print(df_exported_wine[c.vine_sold_usd].sum())
    
    #plot_heat_map_weather_and_production(df_produced_wine, df_weather)
    
    

def plot_heat_map_weather_and_production(df_produced_wine: pd.DataFrame, df_weather: pd.DataFrame):
    df_produced_by_year = get_produced_wine_sum_by_year(df_produced_wine)
    df_produced_by_year[c.vine_produced_kg] = df_produced_by_year[c.vine_produced_kg] / 1_000_000
    
    df = pd.merge(df_produced_by_year, df_weather, on= [c.year])
    
    df = df.drop(c.year, axis= 1)
    df = df.rename(columns = {c.vine_produced_kg: "Quantidade de vinho produzida",
                              c.preciptation: "Preciptação média do ano",
                              c.preciptation_total: "Preciptação total do ano",
                              c.temperature_min: "Temperatura mínima do ano",
                              c.temperature_max: "Temperatura máxima do ano",
                              c.temperature: "Temperatura média do ano",
                              c.humidity: "Umidade média do ano"})
    
    corr_matrix = df.corr()
    
    matrix = corr_matrix["Quantidade de vinho produzida"].sort_values()
    sns.heatmap(data = matrix.to_frame(), annot=True, linewidth=.5)
    plt.show()

    
    
    
def somes_china_plots(df_exported_wine):
    df = df_exported_wine
    df['preco_litro'] = df[c.vine_sold_usd]/df[c.vine_exported_kg]
    
    all_but_liberia_lines = df[c.country] == 'China'
    df = df.loc[all_but_liberia_lines]
    
    # plot_best_countries_generic(
    #     df= df,
    #     column_of_best= 'preco_litro',
    #     ylabel= 'Preço médio pago pelo litro em USD',
    #     title= 'Preço litro venda para China ao longo dos anos'
    # )
    
    
    df[c.vine_exported_kg] = df[c.vine_exported_kg]/1_000.0
    plot_best_countries_generic(
        df= df,
        column_of_best= c.vine_exported_kg,
        ylabel= 'Quantidade comprada em milhares de litros',
        title= 'Importação chinesa de vinhos brasileiros ao longo dos anos'
    )
    
    
def plot_producition_related_by_rain(df_produced_wine, df_weather):
    df_produced_by_year = get_produced_wine_sum_by_year(df_produced_wine)
    df_produced_by_year[c.vine_produced_kg] = df_produced_by_year[c.vine_produced_kg] / 1_000_000
    
    df_rain_by_year = df_weather[[c.year, c.preciptation_total]]
    
    df = pd.merge(df_produced_by_year, df_rain_by_year, on= [c.year])
        
    def plot_scatter(df_plot):
        plt.scatter(df_plot[c.vine_produced_kg], df_plot[c.preciptation_total])
        
        plt.ylabel('Preciptação em mm')
        plt.xlabel('Quantidade de vinho produzida em milhares de litros no ano')
        plt.title('Quantidade de vinho produzida com relação a preciptação total no ano')
        
        plt.grid(True)
        plt.show()
        
    def plot_lines(df_plot):
        df_plot[c.preciptation_total] = df_plot[c.preciptation_total]/100
        
        plt.plot(df_plot[c.year], df_plot[c.preciptation_total], label = 'Preciptação total em centenas de mm')
        plt.plot(df_plot[c.year], df_plot[c.vine_produced_kg], label = 'Vinho produzida em milhares de litros')
        
        plt.xlabel('Ano')
        plt.title('Quantidade de vinho produzida com relação a preciptação total no ano')
        
        plt.grid(True)
        plt.legend()
        plt.show()
        
    plot_scatter(df)
    plot_lines(df)
    
    
def get_produced_wine_sum_by_year(df: pd.DataFrame):
    lines_not_total = df[c.vine_category] != df[c.vine_type]
    df = df.loc[lines_not_total]
    df = df[[c.year, c.vine_produced_kg]]
    df = df.groupby(c.year).sum().reset_index()
    return df

def plot_best_importers(df: pd.DataFrame):
    df['preco_litro'] = df[c.vine_sold_usd]/df[c.vine_exported_kg]
    df[c.vine_sold_usd] = df[c.vine_sold_usd]/1_000_000.0
    df[c.vine_exported_kg] = df[c.vine_exported_kg]/1_000.0
    
    plot_best_countries_generic(
        df= df,
        column_of_best= c.vine_sold_usd,
        ylabel= 'Quantidade importada de vinhos em milhões de USD',
        title= 'Maiores pagadores na importação de vinhos brasileiros ao longo dos anos'
    )
    
    plot_best_countries_generic(
        df= df,
        column_of_best= c.vine_exported_kg,
        ylabel= 'Quantidade comprada em milhares de litros',
        title= 'Maiores importadores em peso de vinhos brasileiros ao longo dos anos'
    )
    
    all_but_liberia_lines = df[c.country] != 'Libéria'
    df = df.loc[all_but_liberia_lines]
    
    plot_best_countries_generic(
        df= df,
        column_of_best= 'preco_litro',
        ylabel= 'Quantidade paga por litro de vinho',
        title= 'Melhores pagadores pelos vinhos brasileiros ao longo dos anos'
    )

def plot_best_countries_generic(df,
                      column_of_best,
                      ylabel = None,
                      title = None,
                      number_of_countries = 5,
                      auto_show = True
                      ):
    best_importers_in_liters = get_best_countrys_by(df, column_of_best, number_of_countries)
    
    filter_by_best_importers = df[c.country].isin(best_importers_in_liters)
    df = df.loc[filter_by_best_importers]

    for country in best_importers_in_liters:        
        country_data = df[df[c.country] == country]
        plt.plot(country_data[c.year], 
                 country_data[column_of_best], 
                 label=country)
    
    plt.ylabel(ylabel)
    plt.xlabel('Ano')
    plt.title(title)
    plt.xticks(list(range(2004, 2020, 1)), rotation = 45)
    plt.grid(True)
    plt.legend()
    if(auto_show):
        plt.show()

def get_best_countrys_by(df: pd.DataFrame, 
                         column: str, 
                         number_of_countrys_to_get: int = 5):
    df = df[[c.country, column]]
    df = df.groupby(c.country).sum().reset_index()
    df = df.sort_values(column, ascending= False)
    
    return df.head(number_of_countrys_to_get)[c.country].unique()



if __name__ == "__main__":
    main()

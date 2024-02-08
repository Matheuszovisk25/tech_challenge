import os
import pandas as pd
from pathlib import Path
from utils.iso_country_codes import ISO_3166_CODES_BY_COUNTRY as COUNTRY_CODES
from utils.columns import Columns as c


DATA_FOLDER = f'{Path(__file__).parent.resolve().parent.resolve()}\\Data'

def main():
    pass
    # df_grape = get_grapes_processed_data_df()
    # df_wines = get_wines_agg_df()
    # df_country = get_country_agg_df()
    # df_weather = get_weather_data_df()
    

def get_weather_data_df():
    weather_df = load_weather_df()
    cleaned_df = clean_weather_df(weather_df)
    aggregated_df = aggregate_weather_df(cleaned_df)
    
    return aggregated_df

def load_weather_df():
    csv_files_list = list(get_weather_data_files())
    
    col_names = [c.date, c.hour, c.preciptation_mm, c.pression_at, c.pression_at_max, c.pression_at_min, c.radiation_kj_m, c.temp_celcius, c.temp_orv_celcius, c.temp_max, c.temp_min, c.temp_orv_max, c.temp_orv_min, c.humidity_max_h, c.humidity_min_h, c.humidity_rel_h, c.wind_dir, c.wind_raj, c.wind_vel, c.empty_col]
    
    df_list = [
        pd.read_csv(
            file,
            encoding="ISO-8859-1",
            header=0,
            sep=";",
            skiprows=9,
            na_values="-9999",
            decimal=",",
            engine="python",
            names=col_names
        )
        for file in csv_files_list
    ]
    
    concated_df = pd.concat(df_list, ignore_index=True)
    return concated_df

def get_weather_data_files():
    folder_path = f"{DATA_FOLDER}\\dados meteorológicos"

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file[-3:].lower() == "csv":
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    yield file_path


def clean_weather_df(concated_df):
    col_to_remove = [c.pression_at, c.pression_at_max, c.pression_at_min, c.radiation_kj_m, c.temp_orv_celcius, c.temp_orv_max, c.temp_orv_min, c.humidity_max_h, c.humidity_min_h, c.wind_dir, c.wind_raj, c.wind_vel, c.empty_col, c.hour]
    
    concated_df = concated_df.drop(col_to_remove, axis=1)
    concated_df[f'{c.year}'] = concated_df[f'{c.date}'].str.slice(0, 4).astype('int32')
    concated_df = concated_df.drop(f'{c.date}', axis=1)
    return concated_df


def aggregate_weather_df(concated_df):
    agg_list = [
        {'column': f'{c.preciptation_mm}', 'agg_func': 'mean', 'new_column_name': c.preciptation},
        {'column': f'{c.preciptation_mm}', 'agg_func': 'sum', 'new_column_name': c.preciptation_total},
        {'column': f'{c.temp_min}', 'agg_func': 'min', 'new_column_name': c.temperature_min},
        {'column': f'{c.temp_max}', 'agg_func': 'max', 'new_column_name': c.temperature_max},
        {'column': f'{c.temp_celcius}', 'agg_func': 'mean', 'new_column_name': c.temperature},
        {'column': f'{c.humidity_rel_h}', 'agg_func': 'mean', 'new_column_name': c.humidity}
    ]

    agg_df = pd.DataFrame()

    for agg_dict in agg_list:
        df_agg = concated_df[[f'{c.year}', agg_dict['column']]].groupby([f'{c.year}']).agg(
            agg_dict['agg_func']).rename(
            columns={agg_dict['column']: agg_dict['new_column_name']})
        agg_df = pd.concat([agg_df, df_agg], axis=1)

    agg_df = agg_df.reset_index()
    return agg_df


def get_grapes_processed_data_df():
    df_americanas = load_and_format_uvas_processadas_americanas_df()
    df_mesa = load_and_format_uvas_processadas_mesa_df()
    df_viniferas = load_and_format_uvas_processadas_viniferas_df()
    
    return pd.concat([df_americanas, df_mesa, df_viniferas])

def load_and_format_uvas_processadas_mesa_df():
    file_path = f"{DATA_FOLDER}\\Uvas processadas\\ProcessaMesa (até 2018).csv"
    
    col_names = ['numerador',c.grape,c.grape_type] + [f'{c.grape_processed_kg}_{n}' for n in range(1970,2019,1)]

    df = pd.read_csv(file_path, encoding="utf-8", sep=";", engine="python",names=col_names, header=None)
    
    df = df.drop(['numerador'] + [f'{c.grape_processed_kg}_{n}' for n in range(1970,2004,1)], axis=1)
    
    df = df.melt(id_vars=[c.grape,c.grape_type], var_name=c.year, value_name=c.grape_processed_kg)
    df[c.year] = df[c.year].str.replace(f'{c.grape_processed_kg}_', '').astype('int32')
    
    df[c.grape_category] = 'Uvas de mesa'
    
    def set_type(row):
        if row[c.grape][:3] == 'ti_':
            return 'TINTAS'
        elif row[c.grape][:3] == 'br_':
            return 'BRANCAS'
        else:
            return row[c.grape]

    old_df = df.copy()
    df[c.grape_type] = df.apply(set_type, axis=1)
    df[c.grape] = old_df[c.grape_type]
    
    return df
    

def load_and_format_uvas_processadas_viniferas_df():
    file_path = f"{DATA_FOLDER}\\Uvas processadas\\ProcessaViniferas (até 2018).csv"
    
    col_names = ['numerador',c.grape,c.grape_type] + [f'{c.grape_processed_kg}_{n}' for n in range(1970,2019,1)]

    df = pd.read_csv(file_path, encoding="utf-8", sep=";", engine="python",names=col_names, header=None)
    
    df = df.drop(['numerador'] + [f'{c.grape_processed_kg}_{n}' for n in range(1970,2004,1)], axis=1)
    
    df = df.melt(id_vars=[c.grape,c.grape_type], var_name=c.year, value_name=c.grape_processed_kg)
    df[c.year] = df[c.year].str.replace(f'{c.grape_processed_kg}_', '').astype('int32')
    
    df[c.grape_category] = 'Viníferas'
    
    def set_type(row):
        if row[c.grape][:3] == 'ti_':
            return 'TINTAS'
        elif row[c.grape][:3] == 'br_':
            return 'BRANCAS E ROSADAS'
        else:
            return row[c.grape]

    old_df = df.copy()
    df[c.grape_type] = df.apply(set_type, axis=1)
    df[c.grape] = old_df[c.grape_type]
    
    return df
    

def load_and_format_uvas_processadas_americanas_df():
    file_path = f"{DATA_FOLDER}\\Uvas processadas\\ProcessaAmericanas (até 2018).csv"
    
    col_names = ['numerador',c.grape,c.grape_type] + [f'{c.grape_processed_kg}_{n}' for n in range(1970,2019,1)]

    df = pd.read_csv(file_path, encoding="utf-8", sep=";", engine="python",names=col_names, header=None)
    
    df = df.drop(['numerador'] + [f'{c.grape_processed_kg}_{n}' for n in range(1970,2004,1)], axis=1)
    
    df = df.melt(id_vars=[c.grape,c.grape_type], var_name=c.year, value_name=c.grape_processed_kg)
    df[c.year] = df[c.year].str.replace(f'{c.grape_processed_kg}_', '').astype('int32')
    
    df[c.grape_category] = 'Americanas e híbridas'
    
    def set_type(row):
        if row[c.grape][:3] == 'ti_':
            return 'TINTAS'
        elif row[c.grape][:3] == 'br_':
            return 'BRANCAS E ROSADAS'
        else:
            return row[c.grape]

    old_df = df.copy()
    df[c.grape_type] = df.apply(set_type, axis=1)
    df[c.grape] = old_df[c.grape_type]
    
    return df
    

def get_country_agg_df():
    population_df = load_and_format_population_by_country_df()
    gdp_df = load_and_format_gdp_by_country_df()

    df = pd.merge(population_df, gdp_df, on= [c.code, c.year])
    
    return df
    
    
def load_and_format_gdp_by_country_df():
    file_path = f"{DATA_FOLDER}\\gdp_per_country_by_year.csv"
    
    df = pd.read_csv(file_path, encoding="utf-8", sep=",", engine="python", decimal='.')
    
    df = df.drop(['Series Name', 'Series Code', 'Country Name'], axis=1)
    df = df.rename(columns = {'Country Code': c.code})
    
    df = df.melt(id_vars=c.code, var_name=c.year, value_name=c.gdp)
    df[c.year] = df[c.year].astype('int32')
    
    df = df.drop(df[df[c.year] < 2004].index)
    df = df.drop(df[df[c.year] > 2019].index)
    
    return df

def load_and_format_population_by_country_df():
    file_path = f"{DATA_FOLDER}\\population_by_countr_per_year.csv"
    
    col_names = [c.country, c.code, c.year, c.population]
    df = pd.read_csv(file_path, encoding="utf-8", sep=",", engine="python",names=col_names, header=None, skiprows=1)
    df[c.year] = df[c.year].astype('int32')
    
    df = df.drop(c.country, axis = 1)
    df = df.drop(df[df[c.year] < 2004].index)
    df = df.drop(df[df[c.year] > 2019].index)
    
    return df

def get_wines_agg_df():
    exported_vinho_df = load_and_format_exp_vinho_df()
    produced_vinho_df = load_and_format_producao_vinho_df()

    df = pd.merge(exported_vinho_df, produced_vinho_df, on= c.year)
    
    return df

def load_and_format_exp_vinho_df():
    file_path = f"{DATA_FOLDER}\\ExpVinho.csv"

    col_names = ['numerador',c.country] + flatten_list([[f'{c.vine_exported_kg}_{n}', f'{c.vine_sold_usd}_{n}'] for n in range(1970,2020,1)])

    df = pd.read_csv(file_path, encoding="utf-8", sep=";", engine="python",names=col_names, header=None)
    
    df = df.drop(['numerador'] + flatten_list([[f'{c.vine_exported_kg}_{n}', f'{c.vine_sold_usd}_{n}'] for n in range(1970,2004,1)]), axis=1)

    df = df.groupby(c.country).sum().reset_index()
    
    df_population = df.melt(id_vars=c.country, value_vars=[f'{c.vine_exported_kg}_{n}' for n in range(2004,2020,1)], var_name=c.year, value_name=c.vine_exported_kg)
    df_population[c.year] = df_population[c.year].str.replace(f'{c.vine_exported_kg}_', '').astype('int32')

    df_gdp = df.melt(id_vars=c.country, value_vars=[f'{c.vine_sold_usd}_{n}' for n in range(2004,2020,1)], var_name=c.year, value_name=c.vine_sold_usd)
    df_gdp[c.year] = df_gdp[c.year].str.replace(f'{c.vine_sold_usd}_', '').astype('int32')

    df = pd.merge(df_population, df_gdp, on= [c.country, c.year])
    
    df[c.code] = df[c.country].map(COUNTRY_CODES)

    return df
    
def load_and_format_producao_vinho_df():
    file_path = f"{DATA_FOLDER}\\Producao.csv"
    
    id_colunms = [c.vine_type,c.vine_category]
    col_names = id_colunms + [f'{c.vine_produced_kg}_{n}' for n in range(1970,2020,1)]
    
    df = pd.read_csv(file_path, encoding="utf-8", sep=";", engine="python",names=col_names, header=None)

    df = df.drop([f'{c.vine_produced_kg}_{n}' for n in range(1970,2004,1)], axis=1)
    
    not_wine_related_colunms = ['SUCO', 'su_Suco de uva simples', 'su_Suco concentrado', 'su_Suco de uva adoçado', 'su_Suco de uva reconstituído', 'DERIVADOS', 'de_Espumante', 'de_Espumante moscatel', 'de_Base espumante', 'de_Base espumante moscatel', 'de_Base Champenoise champanha', 'de_Base Charmat champanha', 'de_Bebida de uva', 'de_Polpa de uva', 'de_Mosto simples', 'de_Mosto concentrado', 'de_Mosto de uva com bagaço', 'de_Mosto dessulfitado', 'de_Mistelas', 'de_Néctar de uva', 'de_Licorosos', 'de_Compostos', 'de_Jeropiga', 'de_Filtrado', 'de_Frisante', 'de_Vinho leve', 'de_Vinho licoroso', 'de_Brandy', 'de_Destilado', 'de_Bagaceira', 'de_Licor de bagaceira', 'de_Vinagre', 'de_Borra líquida', 'de_Borra seca', 'de_Vinho Composto', 'de_Pisco', 'de_Outros derivados']
    df = df.drop(df[df[c.vine_type].isin(not_wine_related_colunms)].index)
    
    df = df.melt(id_vars=id_colunms, var_name=c.year, value_name=c.vine_produced_kg)
    df[c.year] = df[c.year].str.replace(f'{c.vine_produced_kg}_', '').astype('int32')


    def set_type(row):
        if row[c.vine_type][:3] == 'vm_':
            return 'VINHO DE MESA'
        elif row[c.vine_type][:3] == 'vv_':
            return 'VINHO FINO DE MESA (VINÍFERA)'
        else:
            return row[c.vine_type]

    df[c.vine_category] = df.apply(set_type, axis=1)

    remove_underline_from_type = lambda x: x.split('_')[-1]
    df[c.vine_type] = df[c.vine_type].apply(remove_underline_from_type)
    
    return df    


def flatten_list(list_to_flat):
    return [j for sub in list_to_flat for j in sub]

if __name__ == '__main__':
    main()
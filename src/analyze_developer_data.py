import pandas as pd


# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_csv("data/output/items.csv")
df_steam_games = pd.read_csv("data/output/steam_games.csv")



def analyze_developer_data(desarrolladora: str):
    # Creamos un DataFrame más reducido
    df_end1 = df_steam_games.loc[:,['developer', 'id', 'price','release_date']]
    # Utiliza el método str.split para dividir la fecha en sus componentes (Año, Mes, Día) dejando solo el año
    df_end1['release_date'] = df_end1['release_date'].str.split('-').str.get(0)
    # Filtra el DataFrame para los juegos de la empresa desarrolladora especificada
    juegos_desarrolladora = df_end1[df_end1['developer'] == desarrolladora]
    # Agrupa por año y cuenta la cantidad de juegos
    juegos_por_ano = juegos_desarrolladora.groupby('release_date').size().reset_index(name='Cantidad de Items')
    # Filtra los juegos gratuitos
    juegos_gratuitos = juegos_desarrolladora[juegos_desarrolladora['price'] == 0]
    # Agrupa los juegos gratuitos por año y cuenta la cantidad
    juegos_gratuitos_por_ano = juegos_gratuitos.groupby('release_date').size().reset_index(name='cantidad_juegos_gratuitos')
    # Combina los datos de juegos totales y juegos gratuitos por año
    resultado = pd.merge(juegos_por_ano, juegos_gratuitos_por_ano, on='release_date', how='left')
    # Rellena los valores nulos en juegos gratuitos con 0
    resultado['cantidad_juegos_gratuitos'].fillna(0, inplace=True)
    # Calcula el porcentaje de juegos gratuitos por año
    resultado['porcentaje_juegos_gratuitos'] = (resultado['cantidad_juegos_gratuitos'] / resultado['Cantidad de Items']) * 100
    # Elimina la columna 'cantidad_juegos_gratuitos'
    resultado.drop(columns='cantidad_juegos_gratuitos', inplace=True)
    # Renombra las columnas
    resultado.rename(columns={'release_date': 'Año', 'porcentaje_juegos_gratuitos': 'Contenido Free'}, inplace=True)
    # Convierte la columna 'Cantidad de Items' a enteros y 'Contenido Free' a flotantes
    resultado['Cantidad de Items'] = resultado['Cantidad de Items'].astype(int)
    resultado['Contenido Free'] = resultado['Contenido Free'].astype(float)
    # Convierte el DataFrame a una lista de diccionarios para asegurarse de que los tipos de datos sean estándar de Python (evita errores en FastAPI)
    resultado_dict_list = resultado.to_dict(orient='records')
    return resultado_dict_list



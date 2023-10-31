import pandas as pd


# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_csv("data/output/items.csv")
df_steam_games = pd.read_csv("data/output/steam_games.csv")



def developer_endpoint(desarrolladora):

    #Filtrar las reseñas por el desarrollador dado
    reseñas_desarrolladora = df_reviews[df_reviews['user_id'].isin(df_items[df_items['item_id'].isin(df_steam_games[df_steam_games['developer'] == desarrolladora]['id'])]['user_id'])]

    # Contar las reseñas con sentimiento positivo y negativo
    sentimiento_positivo = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_analysis'] == 2].shape[0]
    sentimiento_negativo = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_analysis'] == 0].shape[0]

    # Crear el diccionario de resultados
    resultado = {desarrolladora: {'Positive': sentimiento_positivo, 'Negative': sentimiento_negativo}}

    return resultado
import pandas as pd

# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_csv("data/output/items.csv")
df_steam_games = pd.read_csv("data/output/steam_games.csv")



def UserData(user_id: str):
    # Convierte user_id a tipo str
    user_id = str(user_id)

#Filtra las compras del usuario en df_items
    compras_usuario = df_items[df_items['user_id'] == user_id]

#Combina la información de las compras con los datos de los juegos en df_steam_games
    compras_usuario = pd.merge(compras_usuario, df_steam_games, left_on='item_id', right_on='id', how='inner')

    # Asegura que 'price' sea tratada como tipo numérico (para evitar errores de suma)
    compras_usuario['price'] = pd.to_numeric(compras_usuario['price'], errors='coerce')

#Calcula el gasto total del usuario
    gasto_total = compras_usuario['price'].sum()

#Filtra las revisiones del usuario en df_reviews
    revisiones_usuario = df_reviews[(df_reviews['user_id'] == user_id) & (df_reviews['item_id'].isin(compras_usuario['item_id']))]

#alcula el porcentaje de recomendación positiva
    porcentaje_recomendacion = (revisiones_usuario['recommend'].sum() / len(revisiones_usuario)) * 100

#Calcula la cantidad de ítems comprados
    cantidad_items = len(compras_usuario)

#Devuelve las estadísticas
    return {
        'Gasto Total': round(gasto_total, 2),
        'Porcentaje de Recomendación Promedio': porcentaje_recomendacion,
        'Cantidad de Ítems': cantidad_items
    }



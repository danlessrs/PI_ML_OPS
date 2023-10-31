import pandas as pd



# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_csv("data/output/items.csv")
df_steam_games = pd.read_csv("data/output/steam_games.csv")





def UserForGenre(genero: str):
    # Filtra df_steam_games para obtener solo las filas que contienen el género especificado
    filtered_games = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False)]

    # Filtra df_items para reducir el conjunto de datos a las columnas necesarias
    df_items_filtered = df_items[df_items['item_id'].isin(filtered_games['id'])]

    # Realiza una unión (join) para incluir la información de 'release_date' desde df_steam_games
    df_items_filtered = df_items_filtered.merge(filtered_games[['id', 'release_date']], left_on='item_id', right_on='id', how='inner')

    # Verifica si 'release_date' está en el DataFrame df_items_filtered
    if 'release_date' not in df_items_filtered.columns:
        return {"Error": "La columna 'release_date' no está presente en el DataFrame."}

    # Continúa con la operación de agrupación
    result_df = df_items_filtered.groupby(['user_id', 'release_date'])['playtime_forever'].sum().reset_index()
    max_user = result_df.loc[result_df['playtime_forever'].idxmax()]

    # Convierte las horas jugadas de minutos a horas
    result_df['playtime_forever'] = (result_df['playtime_forever'] / 600).round(0)

    result_df['release_date'] = pd.to_datetime(result_df['release_date'])

    # Luego, puedes extraer el año usando el accessor .dt
    result_df['Año'] = result_df['release_date'].dt.year

    accumulation = result_df.groupby('Año')['playtime_forever'].sum().reset_index()
    accumulation = accumulation.rename(columns={'playtime_forever': 'Horas'})
    accumulation_list = accumulation.to_dict(orient='records')

    return {"Usuario con más horas jugadas para el género " + genero: max_user['user_id'], "Horas jugadas": accumulation_list}



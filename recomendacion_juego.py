import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

# Cargar los datos
df_steam = pd.read_csv('data/output/steam_games.csv')

# Crear una copia del DataFrame para evitar modificar el original
df_steam_copy = df_steam.copy()

# Desanidar las columnas de género
df_steam_copy['genres'] = df_steam_copy['genres'].apply(eval)  # Convierte las listas de géneros en listas de Python
unique_genres = list(set(genre for sublist in df_steam_copy['genres'] for genre in sublist))

# Crear columnas binarias para cada género
mlb = MultiLabelBinarizer()
genre_features = pd.DataFrame(mlb.fit_transform(df_steam_copy['genres']), columns=mlb.classes_)

# Concatenar las características de género con las características de 'specs'
features = pd.concat([genre_features, df_steam_copy['specs'].str.join('|').str.get_dummies()], axis=1)

# Función de recomendación
def recomendacion_juego(id_producto, num_recomendaciones=5):
    # Calcular la similitud coseno entre el juego seleccionado y todos los juegos
    juego_seleccionado = features[features.index == id_producto]
    similaridades = cosine_similarity(juego_seleccionado, features)

    # Obtener los índices de los juegos más similares (excluyendo el juego seleccionado)
    juegos_similares_indices = similaridades.argsort(axis=1)[0][-num_recomendaciones:][::-1]

    # Obtener los nombres de los juegos recomendados (excluyendo el juego seleccionado)
    juegos_recomendados = df_steam_copy.iloc[juegos_similares_indices, :]

    lista = []

    for index, row in juegos_recomendados.iterrows():
        lista.append({"id": row['id'], "title": row['title']})

    return lista
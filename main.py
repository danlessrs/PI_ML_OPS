import pandas as pd
from fastapi import FastAPI
from src.recomendacion_juego import recomendacion_juego
from src.developer_review import developer_endpoint
from src.user_for_genre import UserForGenre
from src.user_data import UserData
from src.analyze_developer_data import analyze_developer_data
from src.best_developer_year import BestDeveloperYear

app = FastAPI()




#Endpoint 1

@app.get("/recomendacion_juego/{id_producto}")
def get_recomendacion_juego(id_producto: int):
    '''Ingresa el ID de un Juego y te recomendara 5 similares. 

    Ejemplo: { recomendaciones': [{ 'id': 679460,'title': 'Morendar: Goblin Slayer'},{'id': 770380,'title': 'Army of Tentacles: (Not) A Cthulhu Dating Sim: Black GOAT of the Woods Edition'}]}

    '''
    result = recomendacion_juego(id_producto) 

    return {"recomendaciones": result}


#Endpoint 2

@app.get("/developer_review/{nombre_desarolladora}")
def developer(nombre_desarolladora: str):
    '''Se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
    
    Ejemplo de retorno: {'Valve' : [Negative = 182, Positive = 278]}
    '''
    
    return developer_endpoint(nombre_desarolladora)


#Endpoint 3

@app.get("/user_for_genre/{genero}")
def user_for_genre(genero: str):
    '''
    Devuelve el ID  del usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.


    Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    
    '''
    resultado = UserForGenre(genero)
    return resultado



#Entpoint 4

@app.get("/user_data/{user_id}")
def user_data(user_id:str):

    '''
    Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

    
    '''
    resultado = UserData(user_id)
    return resultado


@app.get('/developer_data/{nombre_desarrolladora}')
def developer_data(nombre_desarrolladora: str):

    '''
    Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
    
    '''

    resultado = analyze_developer_data(nombre_desarrolladora)
    return resultado
    

@app.get("/best_developer_year/{year}")
def best_developer_year(year: int):

    '''
    
    Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos).
    
    '''

    resultado = BestDeveloperYear(year)
    return resultado

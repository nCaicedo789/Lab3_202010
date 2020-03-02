"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import map as map
from DataStructures import listiterator as it


"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de peliculas. Retorna el catalogo inicializado.
    """
    catalog = {'MovieList':None, 'Directors':None, 'MovieMap': None, 'Actors':None}
    catalog['MovieList'] = lt.newList("ARRAY_LIST")
    catalog['MovieMap_title'] = map.newMap (164531, maptype='CHAINING')#329044 books
    catalog['MovieMap_id'] = map.newMap (164531, maptype='CHAINING')#329044 books
    catalog['Directors_name'] = map.newMap (45767, maptype='CHAINING') #85929 authors
    catalog['Directors_id'] = map.newMap (164531, maptype='CHAINING') #85929 authors
    catalog['Actors'] = map.newMap(130439,maptype='CHAINING')# 260861 actors
    catalog['generos'] = map.newMap(130439,maptype='CHAINING')
    return catalog


def newMovie (row):
    """
    Crea una nueva estructura para almacenar los actores de una pelicula 
    """
    x= row['genres'].split('|')
    book = {"id": row['id'], "title":row['title'], "vote_average":row['vote_average'], "vote_count":row['vote_count'], 'genero':x}
    return book



def addMovieList (catalog, row):
    """
    Adiciona libro a la lista
    """
    books = catalog['MovieList']
    book = newMovie(row)
    lt.addLast(books, book)

def addMovieMap (catalog, row):
    """
    Adiciona libro al map con key=title
    """
    books = catalog['MovieMap_title']
    books_id= catalog['MovieMap_id']
    book = newMovie(row)
    map.put(books, book['title'], book, compareByKey)
    map.put(books_id, book['id'], book, compareByKey)

def newDirector (name, row, catalog):
    """
    Crea una nueva estructura para modelar un autor y sus libros
    """
    author = {'name':"", "DirectorMovies":None,  "Movie_more_6":0, 'id':0, 'sum_aver':0}
    author['id']= row['id']
    author ['name'] = name
    author ['DirectorMovies'] = lt.newList('SINGLE_LINKED')
    author['sum_aver']+= float(map.get(catalog['MovieMap_id'],row['id'],compareByKey)['vote_average'])
    lt.addLast(author['DirectorMovies'],row['id'])
    if float(map.get(catalog['MovieMap_id'],row['id'],compareByKey)['vote_average'])>=6:
        author['Movie_more_6']+=1
    return author

def addDirector_name (catalog, row):
    """
    Adiciona un autor al map y sus libros
    """
    name= row['director_name']
    
    if map.contains(catalog['Directors_name'],name, compareByKey):
        author_1=map.get(catalog['Directors_name'],name,compareByKey)
        lt.addLast(author_1['DirectorMovies'],row['id'])
        author_1['sum_aver']+= float(map.get(catalog['MovieMap_id'],row['id'],compareByKey)['vote_average'])
        if float(map.get(catalog['MovieMap_id'],row['id'],compareByKey)['vote_average'])>=6:
            author_1['Movie_more_6']+=1
    else:
        author_2 = newDirector(name, row, catalog)
        map.put(catalog['Directors_name'], author_2['name'], author_2, compareByKey)

def addDirector_id (catalog, row):
    """
    Adiciona un autor al map y sus libros
    """
    name= row['id']
    
    if map.contains(catalog['Directors_id'],name, compareByKey):
        author_1=map.get(catalog['Directors_id'],name,compareByKey)
        lt.addLast(author_1['DirectorMovies'],row['id'])
        
    else:
        author_2 = newDirector(row['director_name'], row, catalog)
        map.put(catalog['Directors_id'], author_2['id'], author_2, compareByKey)

def newActor (name, row, catalog):
    """
    Crea una nueva estructura para modelar un autor y sus libros
    """
    actor = {'name':"", "ActorMovies":None}
    actor ['name'] = name
    actor ['ActorMovies'] = lt.newList('SINGLE_LINKED')
    lt.addLast(actor['ActorMovies'],row['id'])
    return actor
def addActor (catalog, row):
    """
    Adiciona un autor al map y sus libros
    """
    actors=['actor1_name','actor2_name','actor3_name','actor4_name','actor5_name']
    for x in actors:
        name= row[x]
        if name:
    
            if map.contains(catalog['Actors'],name, compareByKey):
                author_1=map.get(catalog['Actors'],name,compareByKey)
                lt.addLast(author_1['ActorMovies'],row['id'])
        
            else:
                author_2 = newActor(name, row, catalog)
                map.put(catalog['Actors'], author_2['name'], author_2, compareByKey)

# Funciones de consulta


def getBookInList (catalog, bookTitle):
    """
    Retorna el libro desde la lista a partir del titulo
    """
    pos = lt.isPresent(catalog['booksList'], bookTitle, compareByTitle)
    if pos:
        return lt.getElement(catalog['booksList'],pos)
    return None


def getBookInMap (catalog, bookTitle):
    """
    Retorna el libro desde el mapa a partir del titulo (key)
    """
    return map.get(catalog['booksMap'], bookTitle, compareByKey)


def getAuthorInfo (catalog, authorName):
    """
    Retorna el autor a partir del nombre
    """
    return map.get(catalog['authors'], authorName, compareByKey)

# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

def get_movies_by_director(catalog, name):
    return map.get(catalog['Directors'],name, compareByKey)['Movie_more_6']

def get_movies_by_title(catalog, name):
    x= map.get(catalog['MovieMap_title'],name, compareByKey)
    if x:
        vote=x['vote_average']
        votos_totales= x['vote_count']
        director_id= x['id']
        director= map.get(catalog['Directors_id'],director_id, compareByKey)['name']
        return ('El numero de votos es: ',str(votos_totales),'\nEl promedio de votos es: ',str(vote),'\nEl director de la pelicula es: ',str(director))
    else:
        return 'No se encontro la pelicula'

def get_director_info(catalog, name):
    director= map.get(catalog['Directors_name'],name,compareByKey)
    if director:
        num_peli= lt.size(director['DirectorMovies'])
        vote_aver= director['sum_aver']/num_peli
        peliculas=[]
        for i in range (1, num_peli+1):
            id=lt.getElement(director['DirectorMovies'],i)
            peliculas.append(map.get(catalog['MovieMap_id'],id, compareByKey)['title'])            
        return ('El director ', name, 'a dirigido ',str(num_peli),' peliculas con un voto promedio de ',str(vote_aver),' las peliculas del director son:\n', str(peliculas))
    else:
        return 'No se encontro el director'


def get_movies_by_actor(catalog, name):
    return map.get(catalog['Actors'], name, compareByKey)["ActorMovies"]

def get_generos(catalog, gen):
    x= map.keySet(catalog['MovieMap_id'])
    numero=0
    for j in range (1, lt.size(x)+1):
        elemento= lt.getElement(x, j)
        genros= map.get(catalog['MovieMap_id'], elemento, compareByKey)['genero']
        for i in generos:
            if i == gen:
                numero+=1
    return numero



    



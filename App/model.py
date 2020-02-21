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
    catalog['Directors'] = map.newMap (45767, maptype='CHAINING') #85929 authors
    catalog['Actors'] = map.newMap(130439,maptype='CHAINING')# 260861 actors
    return catalog


def newMovie (row):
    """
    Crea una nueva estructura para almacenar los actores de una pelicula 
    """
    book = {"id": row['id'], "title":row['title'], "vote_average":row['vote_average'], "vote_count":row['vote_count']}
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
    author = {'name':"", "DirectorMovies":None,  "Movie_more_6":0}
    author ['director_name'] = name
    author ['DirectorMovies'] = lt.newList('SINGLE_LINKED')
    lt.addLast(author['DirectorMovies'],row['id'])
    if map.get(catalog['MovieMap_id'],row['id'],compareByKey)['vote_average']>=6:
        author['Movie_more_6']+=1
    return author

def addDirector (catalog, name, row):
    """
    Adiciona un autor al map y sus libros
    """
    if name:
        authors = catalog['Directors']
        author=map.get(authors,name,compareByKey)
        if author:
            lt.addLast(author['DirectorMovies'],row['id'])
            if map.get(catalog['MovieMap_id'],row['id'],compareByKey)['vote_average']>=6:
                author['Movie_more_6']+=1
        else:
            author = newDirector(name, row, catalog)
            map.put(authors, author['name'], author, compareByKey)


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

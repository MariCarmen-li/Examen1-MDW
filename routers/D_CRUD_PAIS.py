from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import csv


class Pais (BaseModel):
    id: int
    pais: str
    region: str


paises_lista = []


with open('CountryTable.csv') as archivo:
    reader = csv.reader(archivo)
    for i, row in enumerate(reader):
        if (i != 0):  # Imite el primer elemento porque es el encabezado
            aux = Pais(id=i, pais=row[1], region=row[3])
            paises_lista.append(aux)

#CRUD-router
routerPaises = APIRouter()

#Get con Filtro por region
@routerPaises.get("/{_region}/",status_code=status.HTTP_200_OK)
async def read(_region: str):
    paisessolo = filter(lambda pais:  pais.region == _region, paises_lista)
    try:
        return list(paisessolo)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#Get con Filtro por region y id
@routerPaises.get("/{_region}/{_id}",status_code=status.HTTP_200_OK)
async def read(_region: str, _id: int):
    paises_por_region = filter(lambda paises:  paises.region == _region, paises_lista)
    pais_por_id = filter(lambda pais: pais.id == _id, list(paises_por_region))
    try:
        return list(pais_por_id)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
#Post (Create)
#Ejemplo para acción post.
#   path: /Caribbean/
#   result: {
#               id: <id>
#               nombre: <nombre>
#               region: Caribbean
#           }
#Es decir, el nombre de la región en el path sera la región asignada al nuevo país creado en el post
@routerPaises.post("/{_region}/", response_model= Pais, status_code=status.HTTP_201_CREATED)
async def create(nuevoPais: Pais, _region: str):
    for paisAux in paises_lista:
        if paisAux.id == nuevoPais.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Id repetido")
    else:
        nuevoPais.region = _region
        paises_lista.append(nuevoPais)
        return nuevoPais

#Put (update)
#Ejemplo para acción put.
#   path: /Caribbean/
#   result: {
#               id: <id>
#               nombre: <nombre>
#               region: <nuevo_region>
#           }
#Aquí todos los datos se actualizan
@routerPaises.put("/{_region}/", response_model=Pais, status_code=status.HTTP_201_CREATED)
async def update(nuevoPais: Pais):
    found = False
    for index, saved_pais in enumerate(paises_lista):
        if saved_pais.id == nuevoPais.id:
            paises_lista[index] = nuevoPais
            found = True
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El país no existe")
    else:
        return nuevoPais
    
#Delete
#Ejemplo para acción delete.
#   path: /Caribbean/{id}
#   result: Se borra todo el objeto
#Aquí funciona igual cualsea 
@routerPaises.delete("/{_region}/{_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(_region: str, _id: int):#La región la pedimos solo para verificar que no este vacio, el id para borrar el objeto
    found = False
    for index, saved_pais in enumerate(paises_lista):
        if saved_pais.id == _id:
            del paises_lista[index]
            found = True
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id no econtrado")

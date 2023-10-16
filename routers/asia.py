
#Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import APIRouter, HTTPException, status
#Importamos pydantic para obtener una entidad que pueda definir usuarios
from pydantic import BaseModel
import csv
            
class Regiones (BaseModel):
    Id: int
    Region:str

regiones_lista=[
                Regiones(Id = 1, Region = "Middle East"),
                Regiones(Id = 2, Region = "Southern and Central Asia"),
                Regiones(Id = 3, Region = "Southeast Asia"),
                Regiones(Id = 4, Region = "Eastern Asia")
                ]

routerRegiones = APIRouter()

 
#Función Get:
@routerRegiones.get("/asia/",status_code=status.HTTP_200_OK)
async def asia():
    return regiones_lista

@routerRegiones.get("/asia/{id}", status_code=status.HTTP_200_OK)
async def asia(id: int):
    region = filter(lambda regiones: regiones.Id == id, regiones_lista)
    try:
        return list(region)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
#Función Post (Create). Es decir, crea un nuevo usuario. Implementamos también el código de respuesta
@routerRegiones.post("/asia/", response_model=Regiones, status_code=status.HTTP_201_CREATED)
async def asia(region:Regiones):
    
    
    for saved_regiones in regiones_lista:
        if saved_regiones.Id == region.Id:  #Si el Id del usuario guardado es igual al Id del usuario nuevo
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="La region ya existe")
    else:
        regiones_lista.append(region)
        return region
    
    #***Put (update). Es decir, de un usuario que YA EXISTE, lo va a modificar
@routerRegiones.put("/asia/", response_model=Regiones, status_code=status.HTTP_201_CREATED)
async def asia(region:Regiones):
    
    found=False     #Usamos bandera found para verificar si hemos encontrado el usuario 
    
    for index, saved_regiones in enumerate(regiones_lista):
        if saved_regiones.Id == region.Id:  #Si el Id del usuario guardado es igual al Id del usuario nuevo
           regiones_lista[index] = region  #accedemos al indice de la lista que hemos encontrado y actualizamos con el nuevo usuario
           found=True
           
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return region
    
    
        #***Delete
@routerRegiones.delete("/asia/{id}", status_code=status.HTTP_204_NO_CONTENT) #Aquí no es necesario poner todo el usuario, con el id basta para eoncontrarlo y eliminarlo
async def asia(id:int):
    
    found=False     #Usamos bandera found para verificar si hemos encontrado el usuario 
    
    for index, saved_regiones in enumerate(regiones_lista):
        if saved_regiones.Id == id:  #Si el Id del usuario guardado es igual al Id del usuario nuevo
           del regiones_lista[index]  #Eliminamos al indice de la lista que hemos encontrado 
           found=True
           #El código 204 por naturaleza no devuelve nada, solo indica el éxito
       
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
    

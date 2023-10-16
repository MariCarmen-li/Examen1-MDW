
#Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import APIRouter, HTTPException, status
#Importamos pydantic para obtener una entidad que pueda definir usuarios
from pydantic import BaseModel
import csv

routerPaises = APIRouter()


class Paises (BaseModel):
    Id: int
    code: str
    name: str
    surface_area: str
    population: int
    life_expectancy: str
    local_name: str
    government_form: str
    head_of_state: str

#Leemos los datos del csv y los pasamos a una lista#
paises_list=[]

with open('CountryTable.csv') as archivo:
    reader = csv.reader(archivo)
    for i, row in enumerate(reader):
        #[0]=code, [1]=name, [2]=continent, [3]=region, [4]=surface_area, [5]=independence_year, [6]=population, 
        # [7]=life_expectancy, [8]gnp, [9]=gnp_old, [10]=local_name, [11]=government_form, [12]=head_of_state
        # [13]=capital, [14]=code2
        if(i != 0):
            aux = Paises(
                Id = i,
                code=row[0],
                name=row[1],
                surface_area=row[4],
                population=row[6],
                life_expectancy=row[7],
                local_name=row[10],
                government_form=row[11],
                head_of_state=row[12]
                )
            paises_list.append(aux)
 
    #code,name,continent,region,surface_area,independence_year,population,life_expectancy,
#gnp,gnp_old,local_name,government_form,head_of_state,capital,code2

#Función Get:
@routerPaises.get("/continent/region/country/", status_code=status.HTTP_200_OK)
async def paises():
    return paises_list

@routerPaises.get("/continent/region/country/{id}", status_code=status.HTTP_200_OK)
async def paises(id: int):
    region = filter(lambda regiones: regiones.Id == id, paises_list)
    try:
        return list(region)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
#Función Post (Create). Es decir, crea un nuevo usuario. Implementamos también el código de respuesta
@routerPaises.post("/continent/region/country/", response_model=Paises, status_code=status.HTTP_201_CREATED)
async def paises(region:Paises):
        
    for saved_regiones in paises_list:
        if saved_regiones.Id == region.Id:  #Si el Id del usuario guardado es igual al Id del usuario nuevo
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El pais ya existe")
    else:
        paises_list.append(region)
        return region
    
    #http://127.0.0.1:8000/usersclass/

    #***Put (update). Es decir, de un usuario que YA EXISTE, lo va a modificar
@routerPaises.put("/continent/region/country/", response_model=Paises, status_code=status.HTTP_201_CREATED)
async def paises(region:Paises):
    
    found=False     #Usamos bandera found para verificar si hemos encontrado el usuario 
    
    for index, saved_regiones in enumerate(paises_list):
        if saved_regiones.Id == region.Id:  #Si el Id del usuario guardado es igual al Id del usuario nuevo
           paises_list[index] = region  #accedemos al indice de la lista que hemos encontrado y actualizamos con el nuevo usuario
           found=True
           
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return region
    
    #http://127.0.0.1:8000/usersclass/
    
    
        #***Delete
@routerPaises.delete("/continent/region/country/{id}", status_code=status.HTTP_204_NO_CONTENT) #Aquí no es necesario poner todo el usuario, con el id basta para eoncontrarlo y eliminarlo
async def paises(id:int):
    
    found=False     #Usamos bandera found para verificar si hemos encontrado el usuario 
    
    for index, saved_regiones in enumerate(paises_list):
        if saved_regiones.Id == id:  #Si el Id del usuario guardado es igual al Id del usuario nuevo
           del paises_list[index]  #Eliminamos al indice de la lista que hemos encontrado 
           found=True
           #El código 204 por naturaleza no devuelve nada, solo indica el éxito
       
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

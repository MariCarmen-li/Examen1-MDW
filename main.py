from fastapi import FastAPI, HTTPException, status
from routers import A_CRUD_Continentes, Africa, Antarctica, asia, Europe, North_America, Oceania, C_REGIONES, D_CRUD_PAIS, E_CRUD_Paises
from pydantic import BaseModel
import csv

app = FastAPI()

app.include_router(A_CRUD_Continentes.routerContinentes)

app.include_router(asia.routerRegiones)
app.include_router(North_America.routerRegiones)
app.include_router(Africa.routerRegiones)
app.include_router(Antarctica.routerRegiones)
app.include_router(Oceania.routerRegiones)
app.include_router(Europe.routerRegiones)

app.include_router(C_REGIONES.routerRegiones)

app.include_router(D_CRUD_PAIS.routerPaises)

app.include_router(E_CRUD_Paises.routerPaises)

#F)################### GET con todos los atributos de cada país. Usar ID=Code Country ##################
class Pais (BaseModel):
    code: str
    name: str
    surface_area: str
    population: int
    life_expectancy: str
    local_name: str
    government_form: str
    head_of_state: str

#Leemos los datos del csv y los pasamos a una lista#
paises_lista = []
with open('CountryTable.csv') as archivo:
    reader = csv.reader(archivo)
    for i, row in enumerate(reader):
        #[0]=code, [1]=name, [2]=continent, [3]=region, [4]=surface_area, [5]=independence_year, [6]=population, 
        # [7]=life_expectancy, [8]gnp, [9]=gnp_old, [10]=local_name, [11]=government_form, [12]=head_of_state
        # [13]=capital, [14]=code2
        if(i != 0):
            aux = Pais(
                code=row[0],
                name=row[1],
                surface_area=row[4],
                population=row[6],
                life_expectancy=row[7],
                local_name=row[10],
                government_form=row[11],
                head_of_state=row[12]
                )
            paises_lista.append(aux)
###################################################

@app.get("/continent/region/", status_code=status.HTTP_200_OK)
async def read():
    return paises_lista

@app.get("/continent/region/{code}/")
async def read(code: str):
    paises = filter(lambda pais: pais.code == code, paises_lista)
    try:
        return list(paises)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
######################################################################################################
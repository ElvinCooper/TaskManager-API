from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Dict, Any
import itertools
from itertools import count


app = FastAPI()


class Tarea(BaseModel):
    id: Annotated[int,  Field(gt=0)]
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"] = "pendiente"
    
    
class FiltersParams(BaseModel):
    limit: Annotated[int, Field(ge=1)] = 5
    offset: Annotated[int, Field(ge=0)] = 0
    estado: Literal["pendiente", "completado"] = None
    search: Annotated[str, None] = None


class CrearTarea(BaseModel):
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"] = "pendiente"


class TareaResponse(BaseModel):
    id: int
    titulo: str
    estado: str


class TareaUpdate(BaseModel):
    titulo: Annotated[str | None, Field(min_length=3)] = None
    estado: Literal["pendiente", "completado"] = "pendiente"


fake_db: list[Tarea] = [
    Tarea(id=1, titulo= "Estudiar Python", estado= "pendiente"),
    Tarea(id=2, titulo= "Lavar la ropa", estado= "completado"),
    Tarea(id=3, titulo= "Leer un libro", estado= "pendiente"),
    Tarea(id=4, titulo= "Ir al gimnasio", estado= "completado"),
    Tarea(id=5, titulo= "Comprar comida", estado= "pendiente"),
    Tarea(id=6, titulo= "Limpiar el cuarto", estado= "pendiente"),
    Tarea(id=7, titulo= "Pagar cuentas", estado= "completado"),
    Tarea(id=8, titulo= "Llamar a mamá", estado= "pendiente"),
    Tarea(id=9, titulo= "Revisar correo", estado= "pendiente"),
    Tarea(id=10, titulo= "Lavar carro", estado= "pendiente"),
]


#----------------- Logica para generar ids autoincremental -------------------#

max_id_existente = max(tarea.id for tarea in fake_db)
siguiente_id = max_id_existente + 1
id_generator = itertools.count(start=siguiente_id, step=1)

#----- otra forma de trabajar con itertools ----#
id_generator2 = count(start=1)

def generar_siguiente_id() -> int:
    return next(id_generator)



#-----------------------------------------------#


@app.get("/tareas/", response_model=list[Tarea])
def get_tareas(filter_query: Annotated[FiltersParams, Query()]):
    """ Devuelve una lista de tareas filtradas por parametros"""
    if filter_query.estado:
        lista_filtrada = [tarea for tarea in fake_db if filter_query.estado == tarea.estado]
        if filter_query.search:
           match_list = [item for item in lista_filtrada if filter_query.search.lower() in item.titulo.lower()]
           return match_list[filter_query.offset:filter_query.limit]

        return  lista_filtrada[filter_query.offset:filter_query.limit]

    if filter_query.search:
        lista_completa = fake_db[filter_query.offset:filter_query.limit]
        match_list = [item for item in lista_completa if filter_query.search.lower() in item.titulo.lower()]
        return match_list[filter_query.offset:filter_query.limit]\

    #return {"message": fake_db[filter_query.offset:filter_query.limit]}
    lista_completa = fake_db[filter_query.offset:filter_query.limit]
    return lista_completa[filter_query.offset : filter_query.offset + filter_query.limit]


@app.get("/tareas/{id}", response_model=list[Tarea])
def get_tareas(id: int):
    tarea = [item for item in fake_db if id == item.id]
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no existe")
    return tarea


@app.post("/tarea", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def post_tareas(tarea: CrearTarea):

    nuevo_id = int(next(id_generator))
    nueva_tarea_v2: Tarea = Tarea(id=nuevo_id, **tarea.model_dump())

    # nueva_tarea = {
    #     "id": int(next(id_generator)),
    #     "titulo": tarea.titulo,
    #     "estado": tarea.estado
    # }
    fake_db.append(nueva_tarea_v2)

    return nueva_tarea_v2



@app.put("/tarea/{id}")
def put_tareas(id: int, nueva_data: TareaUpdate):
    tarea = next((t for t in fake_db if t.id == id), None)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no existe")

    update_data: Dict[str, Any] = nueva_data.model_dump()

    tarea_actualizada : Tarea = tarea.model_copy(update=update_data)

    return {"tarea actualizada": tarea_actualizada}



@app.delete("/tarea/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tareas(id: int):
    tarea = next((t for t in fake_db if t.id == id), None)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no existe")

    fake_db.remove(tarea)

    return tarea

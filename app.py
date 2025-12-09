from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal



class Tarea(BaseModel):
    id: Annotated[int,  Field(gt=0)]
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"] = "pendiente"
    
    
class FiltersParams(BaseModel):
    limit: Annotated[int, Field(ge=1)] = 5
    offset: Annotated[int, Field(ge=0)] = 0    
    estado: Literal["pendiente", "completado"] = None
    
    
    
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

app = FastAPI()


@app.get("/tareas/")
def get_tareas(filter_query: Annotated[FiltersParams, Query()]):
    ''' validar si recibio el estado en los parametros'''
    if filter_query.estado:
        lista_filtrada = [tarea for tarea in fake_db if tarea.estado == filter_query.estado]
        return  lista_filtrada[filter_query.offset:filter_query.limit]            
    
    return fake_db[filter_query.offset:filter_query.limit]
    
   
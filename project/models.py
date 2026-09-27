from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Oficina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    direccion: str

    # Relación uno-a-muchos: Una oficina contiene varias personas
    personas: List["Persona"] = Relationship(back_populates="oficina")


class Persona(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    puesto: str
    edad: int

    # Clave foránea referenciando a la tabla 'oficina'
    oficina_id: Optional[int] = Field(default=None, foreign_key="oficina.id")

    # Atributo de relación para navegar hacia la Oficina asociada
    oficina: Optional[Oficina] = Relationship(back_populates="personas")
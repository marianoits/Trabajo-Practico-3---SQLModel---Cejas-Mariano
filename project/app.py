from sqlmodel import Session, select
from project.database import create_db_and_tables, engine
from project.models import Oficina, Persona


def create_oficinas_and_personas():
    """CREATE: Alta de oficinas y personas asociadas mediante relaciones."""
    print("\n--- 1. CREANDO OFICINAS Y PERSONAS ---")
    with Session(engine) as session:
        oficina_central = Oficina(
            nombre="Oficina Central", direccion="Av. Colón 1234"
        )
        oficina_norte = Oficina(
            nombre="Sucursal Norte", direccion="Calle Belgrano 456"
        )

        p1 = Persona(
            nombre="Carlos Pérez",
            puesto="Desarrollador Backend",
            edad=29,
            oficina=oficina_central,
        )
        p2 = Persona(
            nombre="Ana Gómez",
            puesto="Diseñadora",
            edad=32,
            oficina=oficina_central,
        )
        p3 = Persona(
            nombre="Lucas Rodríguez",
            puesto="Analista",
            edad=25,
            oficina=oficina_norte,
        )

        session.add(oficina_central)
        session.add(oficina_norte)
        session.add(p1)
        session.add(p2)
        session.add(p3)

        session.commit()
        print(" Oficinas y personas creadas exitosamente.")


def read_personas_de_oficina():
    """READ: Listar personas navegando oficina.personas."""
    print("\n--- 2. READ: Listar personas navegando oficina.personas ---")
    with Session(engine) as session:
        statement = select(Oficina).where(
            Oficina.nombre == "Oficina Central"
        )
        oficina = session.exec(statement).first()

        if oficina:
            print(
                f"Personas en '{oficina.nombre}' ({oficina.direccion}):"
            )
            for persona in oficina.personas:
                print(
                    f" - {persona.nombre} | Puesto: {persona.puesto} | Edad: {persona.edad}"
                )


def read_con_join():
    """READ: Consulta utilizando JOIN entre Persona y Oficina."""
    print("\n--- 3. READ: Consulta con JOIN ---")
    with Session(engine) as session:
        statement = (
            select(Persona, Oficina)
            .join(Oficina)
            .where(Oficina.nombre == "Sucursal Norte")
        )
        results = session.exec(statement).all()

        for persona, oficina in results:
            print(
                f"Empleado: {persona.nombre} -> Pertenece a: {oficina.nombre}"
            )


def read_con_filtro():
    """READ: Filtro con .where() sobre campos de Persona."""
    print("\n--- 4. READ: Consulta con Filtro (.where) ---")
    with Session(engine) as session:
        statement = select(Persona).where(Persona.edad >= 28)
        personas = session.exec(statement).all()

        print("Personas con edad mayor o igual a 28 años:")
        for p in personas:
            print(f" - {p.nombre} ({p.edad} años) - Puesto: {p.puesto}")


def update_reasignar_persona():
    """UPDATE: Reasignar una persona de una oficina a otra."""
    print("\n--- 5. UPDATE: Reasignar persona a otra oficina ---")
    with Session(engine) as session:
        p_statement = select(Persona).where(Persona.nombre == "Carlos Pérez")
        persona = session.exec(p_statement).first()

        o_statement = select(Oficina).where(
            Oficina.nombre == "Sucursal Norte"
        )
        nueva_oficina = session.exec(o_statement).first()

        if persona and nueva_oficina:
            print(
                f"Reasignando a {persona.nombre} a '{nueva_oficina.nombre}'..."
            )
            persona.oficina = nueva_oficina
            session.add(persona)
            session.commit()
            session.refresh(persona)
            print(
                f" Reasignación completa. Nueva oficina: {persona.oficina.nombre}"
            )


def delete_persona():
    """DELETE: Eliminar una persona de la base de datos."""
    print("\n--- 6. DELETE: Eliminar una persona ---")
    with Session(engine) as session:
        statement = select(Persona).where(Persona.nombre == "Ana Gómez")
        persona = session.exec(statement).first()

        if persona:
            print(f"Eliminando a {persona.nombre}...")
            session.delete(persona)
            session.commit()
            print(" Persona eliminada correctamente.")


def main():
    create_db_and_tables()
    create_oficinas_and_personas()
    read_personas_de_oficina()
    read_con_join()
    read_con_filtro()
    update_reasignar_persona()
    delete_persona()


if __name__ == "__main__":
    main()
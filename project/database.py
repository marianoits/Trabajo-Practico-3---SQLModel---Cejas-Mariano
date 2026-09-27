from sqlmodel import SQLModel, create_engine

# Conexión con la base de datos SQLite local
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# engine maneja la conexión con la base de datos
engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    """Crea todas las tablas definidas en los modelos."""
    SQLModel.metadata.create_all(engine)
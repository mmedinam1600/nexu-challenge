from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from loguru import logger

from core.config import settings


class Database:
    def __init__(self, db_url: str):
        """
        Inicializa la conexión a la base de datos.
        Args:
            db_url (str): La URL de conexión a la base de datos.
        """
        logger.info("Inicializando la conexión a la base de datos...")
        try:
            self.engine: Engine = create_engine(db_url, pool_pre_ping=True)

            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

            self.Base = declarative_base()
            logger.success(
                "Instancia de Database creada y motor inicializado correctamente."
            )
        except Exception as e:
            logger.critical(f"Error al inicializar la instancia de Database: {e}")
            raise

    def get_db(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        logger.trace("Abriendo sesión de base de datos.")
        try:
            yield db
        finally:
            db.close()
            logger.trace("Sesión de la base de datos cerrada.")


database = Database(str(settings.POSTGRES_URI))

get_db = database.get_db
Base = database.Base

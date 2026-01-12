import psycopg2
from contextlib import contextmanager
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class DatabaseConnection:
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(Config.get_db_connection_string())
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()

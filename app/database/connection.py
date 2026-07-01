from sqlalchemy import create_engine
from urllib.parse import quote_plus

from app.config.settings import settings

connection_string = (
    f"DRIVER={{{settings.DATABASE_DRIVER}}};"
    f"SERVER={settings.DATABASE_SERVER};"
    f"DATABASE={settings.DATABASE_NAME};"
    "Trusted_Connection=yes;"
)

DATABASE_URL = (
    f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)
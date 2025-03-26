import os
import pyodbc
from dotenv import load_dotenv
from threading import Lock

load_dotenv()

SERVER = os.getenv('SQL_SERVER')
DATABASE = os.getenv('SQL_DB')
USERNAME = os.getenv('SQL_USER')
PASSWORD = os.getenv('SQL_PASS')
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID=sa;PWD={PASSWORD};TrustServerCertificate=yes'

class SingletonDB:
    _instance = None  # Class variable for the singleton instance
    _lock = Lock()    # Thread-safe lock

    def __new__(cls, connection_string):
        if not cls._instance:
            with cls._lock:  # Thread-safe block
                if not cls._instance:  # Double-checked locking
                    cls._instance = super().__new__(cls)
                    cls._instance._connection = pyodbc.connect(connection_string)  # Create the connection
        return cls._instance

    def get_connection(self):
        return self._connection
    
db_instance = SingletonDB(connection_string)
connection = db_instance.get_connection()


KOALA_URL = os.getenv('KOALA_URL')
KOALA_USERNAME = os.getenv('KOALA_USERNAME')
KOALA_PASSWORD = os.getenv('KOALA_PASSWORD')

SPEC_TABLE_NAME = {
    "DEPT": "RelationDept",
    "USER": "UserInfo",
    "LOG_DATA": "CheckInOut"
}

COMPANY_NAME = os.getenv("COMPANY_NAME")
PAGE_SIZE = 100
LATEST_FILE_TXT=os.getenv('LATEST_TIME_SYNC')
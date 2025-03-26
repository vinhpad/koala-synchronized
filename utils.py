from config import *
from datetime import datetime

async def clear_table(table_name):
    query_str = f"""
            DELETE FROM [{table_name}];
        """
    try:
        cursor = connection.cursor()
        cursor.execute(query_str)
        connection.commit()
    except Exception as error:
        connection.rollback()
    finally:
        cursor.close()

def formatted_date_time(timestamp, format_str):
    date_time = datetime.fromtimestamp(timestamp)
    formatted_date_time = date_time.strftime(format_str)
    return formatted_date_time

def getLatestTimeSync():
    with open(LATEST_FILE_TXT, 'r') as file:
        content = file.read()
    return int(content)

def updateLatestTimeSync(timestamp):
    with open(LATEST_FILE_TXT, 'w') as file:
        file.write(str(int(timestamp)))
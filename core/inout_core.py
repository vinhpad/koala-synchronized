from config import connection


async def createCheckInOut(checkinout_data):
    query = """
        INSERT INTO [CheckInOut] (
            [UserEnrollNumber], 
            [TimeStr], 
            [TimeDate], 
            [OriginType]
        ) VALUES (?, ?, ?, ?)
    """
    
    values = checkinout_data

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
    except Exception as error:
        connection.rollback()
    finally:
        cursor.close()


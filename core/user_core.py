
from config import connection

async def createUser(users):
    query = """
        INSERT INTO [UserInfo] (
            [UserEnrollNumber], 
            [UserFullCode], 
            [UserFullName], 
            [UserEnrollName], 
            [UserHireDay], 
            [UserPrivilege],
            [UserEnabled],
            [UserIDD],
            [SchID])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, users)
        connection.commit()
    except Exception as error:
        connection.rollback()
        print(f'Error | {error}')
    finally:
        cursor.close()

async def findUserByUserFullCode(userFullCode):
    query = """
        SELECT TOP (1) [UserEnrollNumber] FROM [UserInfo]
        WHERE [UserFullCode] = (?)
    """
    userEnrollNumber = -1
    try:
        cursor = connection.cursor()
        cursor.execute(query, userFullCode)
        result = cursor.fetchall()
        userEnrollNumber = result[0][0]
        connection.commit()
    except Exception as error:
        connection.rollback()
    finally:
        cursor.close()
        return userEnrollNumber
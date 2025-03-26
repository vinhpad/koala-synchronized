from config import connection

async def createRelationDepts(relation_depts):
    query = f"""
        INSERT INTO [RelationDept] ([Description], [RelationID], [LevelID], [DeptCode], [IsUsedReport]) VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor = connection.cursor()
        cursor.executemany(query, relation_depts)
        connection.commit()
    except Exception as error:
        connection.rollback()
    finally:
        cursor.close()

async def getDeptByDeptCode(dept_code):
    query = f"""
        SELECT * FROM [RelationDept] WHERE [Description] = ?
    """

    data = 1
    try:
        cursor = connection.cursor()
        cursor.execute(query, (dept_code))
        data = cursor.fetchall()[0][0]
        connection.commit()  
    except Exception as error:
        connection.rollback()
    finally:
        cursor.close()
    return data

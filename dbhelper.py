from sqlite3 import connect,Row

database:str = 'skills.db'

def getprocess(sql:str)->list:
    db=connect(database)
    cursor:object = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql)
    data:list = cursor.fetchall()
    db.close()
    return data

def postprocess(sql:str)->list:
    db=connect(database)
    cursor:object = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return True if cursor.rowcount>0 else False

def add_record(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    values:list = list(kwargs.values())
    flds:str = "`,`".join(keys)
    data:str = "','".join(values)
    sql:str = f"INSERT INTO `{table}` (`{flds}`) VALUES ('{data}')"
    return postprocess(sql)

def delete_record(table: str, **kwargs)-> bool:
    keys:list = list(kwargs.keys())
    values:list = list(kwargs.values())
    sql:str = f"DELETE FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
    return postprocess(sql)
    
def getall_records(table:str)->list:
	sql:str = f"SELECT * FROM `{table}`"
	return getprocess(sql)

def getall_books()->list:
    sql:str =f"SELECT isbn,title,author,copyright,edition,price,qty,[price]*[qty] as total FROM `books`"
    return getprocess(sql)

# books:list = getall_books()
# for book in books:
    # print(f"{book[1]}",end=" ")
    # print(f"{book[7]}")

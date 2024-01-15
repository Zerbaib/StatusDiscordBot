import sqlite3

def create_database(db_name):
    """
    Creates a new SQLite database with the given name.
    
    Args:
        db_name (str): The name of the database.
    """
    conn = sqlite3.connect(db_name)
    conn.close()

def create_table(db_name, table_name, columns):
    """
    Creates a new table in the specified database with the given name and columns.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
        columns (list): A list of column names.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    column_str = ', '.join(columns)
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

def del_table(db_name, table_name):
    """
    Deletes the specified table from the database.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    delete_table_query = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(delete_table_query)
    conn.commit()
    conn.close()

def get_data(db_name, table_name, columns, condition=None):
    """
    Retrieves data from the specified table in the database.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
        columns (list): A list of column names.
        condition (str, optional): The condition to filter the rows to be retrieved. Defaults to None.
    
    Returns:
        list: A list of tuples containing the data.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    column_str = ', '.join(columns)
    select_query = f"SELECT {column_str} FROM {table_name}"
    if condition:
        select_query += f" WHERE {condition}"
    cursor.execute(select_query)
    data = cursor.fetchall()
    conn.close()
    return data

def add_data(db_name, table_name, data):
    """
    Adds a new row of data to the specified table in the database.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
        data (tuple): A tuple of values to be inserted into the table.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    placeholders = ', '.join(['?' for _ in range(len(data))])
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

def modify_data(db_name, table_name, column, new_value, condition):
    """
    Modifies the value of a specific column in the specified table based on a condition.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
        column (str): The name of the column to be modified.
        new_value (str): The new value to be set for the column.
        condition (str): The condition to filter the rows to be modified.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    update_query = f"UPDATE {table_name} SET {column} = ? WHERE {condition}"
    cursor.execute(update_query, (new_value,))
    conn.commit()
    conn.close()

def del_data(db_name, table_name, condition):
    """
    Deletes rows from the specified table based on a condition.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
        condition (str): The condition to filter the rows to be deleted.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    delete_query = f"DELETE FROM {table_name} WHERE {condition}"
    cursor.execute(delete_query)
    conn.commit()
    conn.close()

def check_table_exist(db_name, table_name):
    """
    Checks if the specified table exists in the database.
    
    Returns:
        bool: True if the table exists, False otherwise.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    check_table_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    cursor.execute(check_table_query)
    data = cursor.fetchall()
    conn.close()
    if data:
        return True
    return False

def check_data_exist(db_name, table_name, condition):
    """
    Checks if the specified data exists in the table based on a condition.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table.
        condition (str): The condition to filter the rows to be checked.
    
    Returns:
        bool: True if the data exists, False otherwise.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    check_data_query = f"SELECT * FROM {table_name} WHERE {condition}"
    cursor.execute(check_data_query)
    data = cursor.fetchall()
    conn.close()
    if data:
        return True
    return False
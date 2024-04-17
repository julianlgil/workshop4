import uuid


def get_python_type(sql_type):
    if 'int' in sql_type:
        return int
    if 'uuid' in sql_type:
        return uuid.UUID
    if 'varchar' in sql_type:
        return str


def get_sql_type(py_type):
    py_type = str(py_type)
    if 'str' in py_type:
        return 'VARCHAR'
    if 'uuid' in py_type:
        return 'UUID'
    if 'int' in py_type:
        return 'INTEGER'

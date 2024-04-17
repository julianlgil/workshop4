import functools
import os
import uuid
from typing import Type

import psycopg

from abstracts import DAO
from utils import get_python_type, get_sql_type

DSN = os.getenv('DATABASE__DSN')
def persist_db(func):
    @functools.wraps(func)
    def wrapper(self: DAO, *args, **kwargs):
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                statement = f'INSERT INTO {self._table_name} VALUES {tuple(self.__dict__.values())}'
                func(self, *args, **kwargs)
                cur.execute(statement)
                conn.commit()
    return wrapper


def list_all_db(func):
    def set_attributes(klass: Type, data):
        result = []
        for row in data:
            instance = klass()
            i = 0
            for key in klass.__annotations__.keys():
                setattr(instance, key, row[i])
                i += 1
            result.append(instance)
        return result
    @functools.wraps(func)
    def wrapper(self: DAO, *args, **kwargs):
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                statement = f'SELECT * FROM {self._table_name};'
                func(self, *args, **kwargs)
                cur.execute(statement)
                result = cur.fetchall()
                return set_attributes(self, result)
    return wrapper


class Entity(DAO):

    def __init__(self, name: str, pk: str, *args, **kwargs):
        super().__init__()
        self.name = name
        self.pk = pk

    def __call__(self, entity, **kwargs):
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                table_name = self.name
                cur.execute(f"SELECT column_name,udt_name FROM information_schema.columns WHERE table_name = '{table_name}';")
                result = cur.fetchall()
                is_valid_table = self.__validate_table_with_entity(entity, result)
                if not is_valid_table:
                    cur.execute(f"DROP TABLE IF EXISTS {self.name};")
                    query = self.__get_content_creation_query(entity)
                    cur.execute(f"CREATE TABLE {table_name}({query})")
                    conn.commit()
        entity._table_name = self.name
        return entity

    def __get__(self, instance, owner):
        from functools import partial
        return partial(self.__call__, instance)

    def __validate_table_with_entity(self, entity, table):
        entity_annotations = entity.__annotations__
        if len(entity_annotations) != len(table):
            return False
        for key, sql_type in table:
            if key not in entity_annotations:
                return False
            python_type = get_python_type(sql_type)
            if python_type != entity_annotations.get(key):
                return False
        return True

    def __get_content_creation_query(self, entity):
        query = ''
        i = 0
        for key, types in entity.__annotations__.items():
            i = i + 1
            if key == self.pk:
                query += f'{key} {get_sql_type(types)} PRIMARY KEY'
            else:
                query += f'{key} {get_sql_type(types)}'
            if i < len(entity.__annotations__):
                query += ', '
        return query







from typing import Type

from decorators import persist_db, list_all_db
from abstracts import DAO


class Repository:

    def __init__(self, klass: Type[DAO]):
        self.klass = klass

    @staticmethod
    @persist_db
    def persist(entity: DAO):
        print('Persisting class:', type(entity).__name__)

    @staticmethod
    @list_all_db
    def list_all(klass: Type[DAO]):
        print('Getting list of:', klass.__name__)

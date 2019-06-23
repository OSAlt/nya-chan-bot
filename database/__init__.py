from bot.config import Database as DBConfig
from pyArango.connection import Connection, CreationError


class Collection:
    def __init__(self, col):
        self._collection = col

    def enter(self, item, key=None):
        doc = self._collection.createDocument(item)
        doc._key = key
        doc.save()

    def update(self, key, updates):
        doc = self._collection[key]
        for item, value in updates.keys():
            doc[item] = value
        doc.save()

    def entry(self, key):
        return self._collection[key]

    @property
    def entries(self):
        return self._collection.fetchAll()


class Arango:
    def __init__(self):
        conn = Connection(
            arangoURL=f"http://{DBConfig.host}:{DBConfig.port}",
            username=DBConfig.User.name, password=DBConfig.User.password
        )

        try:
            self.database = conn.createDatabase(name=DBConfig.database)
        except CreationError:
            self.database = conn[DBConfig.database]

    def collection(self, name):

        try:
            return Collection(self.database.createCollection(name=name))
        except CreationError:
            return Collection(self.database[name])

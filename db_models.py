import json
import os


class FandomDatabase(object):
    def __init__(self, directory):
        cwd = os.getcwd()
        self.location = os.path.join(cwd, directory, "data.json")
        self._load()

    def _load(self):
        if os.path.exists(self.location):
            self.db = json.load(open(self.location, "r"))
        else:
            self.db = {}
        return True

    def dumpdb(self):
        try:
            json.dump(self.db, open(self.location, "w+"))
            return True
        except:
            return False

    def insert(self, key, value):
        try:
            self.db[str(key)] = value
            self.dumpdb()
            return True
        except Exception as e:
            return False


class FandomPage(object):
    def __init__(self, db, page_id):
        self.db = db
        self.id = page_id
        self._insert()

    def _insert(self):
        self.db.insert(self.id, {})

    def set_content(self, content):
        self.db.insert(self.id, content)

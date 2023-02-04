import json
import os


class FandomDatabase(object):
    def __init__(self, directory, cwd=None):
        if cwd is None:
            cwd = os.getcwd()

        self.location = os.path.join(cwd, directory, "data.json")
        self._load()

    def _load(self):
        if os.path.exists(self.location):
            self.db = json.load(open(self.location, "r", encoding="utf-8"))
        else:
            self.db = {}
        return True

    def dump_to_file(self):
        try:
            json.dump(self.db, open(self.location, "w+", encoding="utf-8"))
            return True
        except:
            return False

    def insert(self, key, value):
        try:
            self.db[str(key)] = value
            self.dump_to_file()
            return True
        except Exception as e:
            return False

    def read_from_file(self):
        try:
            with open(self.location, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None


class Page(object):
    def __init__(self, db, page_id):
        self.db = db
        self.id = page_id
        self._insert()

    def _insert(self):
        self.db.insert(self.id, {})

    def set_content(self, content):
        self.db.insert(self.id, content)

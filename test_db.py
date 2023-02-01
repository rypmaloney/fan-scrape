import os

from jdb_classes import FandomDatabase, Page


def test_FandomDatabase_init(tmpdir):
    directory = "fandom_db"
    tmpdir.mkdir(directory)
    db = FandomDatabase(directory, str(tmpdir))
    assert db.location == tmpdir.join(directory, "data.json").strpath


def test_FandomDatabase_load(tmpdir):
    directory = "fandom_db"
    tmpdir.mkdir(directory)
    db = FandomDatabase(directory)
    assert db._load() == True
    assert db.db == {}


def test_FandomDatabase_insert(tmpdir):
    directory = "fandom_db"
    tmpdir.mkdir(directory)
    db = FandomDatabase(directory, str(tmpdir))
    assert db.insert("foo", "bar") == True
    db.dump_to_file()
    loc = os.path.join(str(tmpdir), directory, "data.json")

    f = open(loc)

    assert f.read() == '{"foo": "bar"}'
    assert db.db == {"foo": "bar"}


def test_Page_init(tmpdir):
    directory = "fandom_db"
    tmpdir.mkdir(directory)
    data_file = tmpdir.join(directory, "data.json")
    data_file.write("{}")
    db = FandomDatabase(directory)
    page = Page(db, "foo")
    assert "foo" in db.db
    assert db.db["foo"] == {}


def test_Page_set_content(tmpdir):
    directory = "fandom_db"
    tmpdir.mkdir(directory)
    db = FandomDatabase(directory, str(tmpdir))
    assert db.insert("foo", "bar") == True
    db.dump_to_file()
    loc = os.path.join(str(tmpdir), directory, "data.json")
    page = Page(db, "foo")

    f = open(loc)
    page.set_content("bar")
    assert f.read() == '{"foo": "bar"}'

    assert db.db == {"foo": "bar"}

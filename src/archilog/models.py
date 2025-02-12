import uuid
import sqlite3

from sqlalchemy import *
from dataclasses import dataclass


@dataclass
class Item:
    id: uuid.UUID
    name: str
    category: str
    value: float


engine = create_engine("sqlite:///storage/archilog.db")
metadata = MetaData()

items = Table(
    "items", metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False),
    Column("category", String, default="unspecified"),
    Column("value", Float, nullable=False)
)

def init_db():
    metadata.create_all(engine)

def insert(id: str, name: str, category: str, value: float):
    db = sqlite3.connect("storage/items.db")
    db.execute("CREATE TABLE IF NOT EXISTS items(id, name, category, value)")

    if id:
        item = Item(uuid.UUID(id), name, category, value)
    else:
        item = Item(uuid.uuid4(), name, category, value)

    if item.category:
        db.execute("INSERT INTO items VALUES (?, ?, ?, ?)",
                   (str(item.id), item.name, item.category, item.value))
    else:
        db.execute("INSERT INTO items (id, name, value) VALUES (?, ?, ?)",
                   (str(item.id), item.name, item.value))

    db.commit()

    return item

def read_where(id: str, name: str, category: str, value: str):
    query = ""
    values = []

    if id:
        query += " WHERE id = ?"
        values.append(id)

        if name:
            query += " AND name = ?"
            values.append(name)

        if category:
            query += " AND category = ?"
            values.append(category)
    elif name:
        query += " WHERE name = ?"
        values.append(name)

        if category:
            query += " AND category = ?"
            values.append(category)
    elif category:
        query += " WHERE category = ?"
        values.append(category)

    return query, values

def select(id: str, name: str, category: str, value: str):
    db = sqlite3.connect("storage/items.db")
    db.execute("CREATE TABLE IF NOT EXISTS items(id, name, category, value)")

    where = read_where(id, name, category, value)
    query, values = "SELECT * FROM items" + where[0], where[1]

    items_table = db.execute(query, values).fetchall()
    nb_selected_rows = 0

    for row in items_table:
        item = Item(row[0], row[1], row[2], row[3])
        nb_selected_rows += 1
        print(item)

    return items_table, nb_selected_rows

def update(id: str, name: str, category: str, value: float,
           new_name: str, new_category: str, new_value: float):
    db = sqlite3.connect("storage/items.db")
    db.execute("CREATE TABLE IF NOT EXISTS items(id, name, category, value)")

    query = "UPDATE items"
    values = []

    if new_name:
        query += " SET name = ?"
        values.append(new_name)

        if new_category:
            query += ", category = ?"
            values.append(new_category)

        if new_value:
            query += ", value = ?"
            values.append(new_value)
    elif new_category:
        query += " SET category = ?"
        values.append(new_category)

        if new_value:
            query += ", value = ?"
            values.append(new_value)
    elif new_value:
        query += " SET value = ?"
        values.append(new_value)

    where = read_where(id, name, category, value)
    query, values = query + where[0], values + where[1]

    db.execute(query, values)
    db.commit()

    return db.total_changes

def delete(id: str, name: str, category: str, value: float):
    db = sqlite3.connect("storage/items.db")
    db.execute("CREATE TABLE IF NOT EXISTS items(id, name, category, value)")

    where = read_where(id, name, category, value)
    query, values = "DELETE FROM items" + where[0], where[1]

    db.execute(query, values)
    db.commit()

    return db.total_changes

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
    if id:
        item = Item(uuid.UUID(id), name, category, value)
    else:
        item = Item(uuid.uuid4(), name, category, value)

    with engine.connect() as conn:
        if item.category:
            ins = items.insert().values(id=item.id, name=item.name, category=item.category, value=item.value)
        else:
            ins = items.insert().values(id=item.id, name=item.name, value=item.value)

        conn.execute(ins)
        conn.commit()

    return item

def select(id: str, name: str, category: str, value: str):
    sel = items.select()

    with engine.connect() as conn:
        if id:
            sel = sel.where(items.c.id == id)

        if name:
            sel = sel.where(items.c.name == name)

        if category:
            sel = sel.where(items.c.category == category)

        if value:
            sel = sel.where(items.c.value == value)

        result = conn.execute(sel)

        items_table = result.fetchall()
        nb_selected_rows = len(items_table)

    return items_table, nb_selected_rows

def update(id: str, name: str, category: str, value: float,
           new_name: str, new_category: str, new_value: float):
    with engine.connect() as conn:
        upd = items.update()

        # WHERE clause
        if id:
            upd = upd.where(items.c.id == id)

        if name:
            upd = upd.where(items.c.name == name)

        if category:
            upd = upd.where(items.c.category == category)

        if value:
            upd = upd.where(items.c.value == value)

        # VALUES clause
        if new_name:
            upd = upd.values(name=new_name)

        if new_category:
            upd = upd.values(category=new_category)

        if new_value:
            upd = upd.values(value=new_value)

        result = conn.execute(upd)
        conn.commit()

        total_changes = result.rowcount

    return total_changes

def delete(id: str, name: str, category: str, value: float):
    db = sqlite3.connect("storage/items.db")
    db.execute("CREATE TABLE IF NOT EXISTS items(id, name, category, value)")

    where = read_where(id, name, category, value)
    query, values = "DELETE FROM items" + where[0], where[1]

    db.execute(query, values)
    db.commit()

    return db.total_changes

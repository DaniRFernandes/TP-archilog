import click

import archilog.models as models
import archilog.services as services


@click.group()
def cli():
    pass

@click.group()
def cli():
    pass

@cli.command()
def init_db():
    models.init_db()
    print("Database created.")

@cli.command()
@click.option("-n", "--name",
              prompt="Name",
              help="The name of the item.")
@click.option("-c", "--category",
              default="Unspecified",
              help="The category of the item.")
@click.option("-v", "--value",
              prompt="Value",
              help="The value of the item.")
def create(name: str, category: str, value: float):
    item = models.insert(None, name, category, value)
    print(f"Inserted item: {item} rows")

@cli.command()
@click.option("-i", "--id",
              help="The ID of the item to read.")
@click.option("-n", "--name",
              help="The name of the items to read.")
@click.option("-c", "--category",
              help="The category of the items to read.")
@click.option("-v", "--value",
              help="The value of the items to read.")
def read(id: str, name: str, category: str, value: str):
    changes = models.select(id, name, category, value)[1]
    print(f"Amount of rows selected: {changes} rows")

@cli.command()
@click.option("-i", "--id",
              help="The ID ('id' field) of the row to update.")
@click.option("-n", "--name",
              help="The 'name' field for the rows to update.")
@click.option("-c", "--category",
              help="The 'category' field for the rows to update.")
@click.option("-v", "--value",
              help="The 'value' field for the rows to update.")
@click.option("--new-name",
              help="The new value for the 'name' field.")
@click.option("--new-category",
              help="The new value for the 'category' field.")
@click.option("--new-value",
              help="The new value for the 'value' field.")
def update(id: str, name: str, category: str, value: float,
           new_name: str, new_category: str, new_value: float):
    changes = models.update(id, name, category, value, new_name, new_category, new_value)
    print(f"Amount of rows updated: {changes} rows")

@cli.command()
@click.option("-i", "--id",
              help="The ID of the item to read.")
@click.option("-n", "--name",
              help="The name of the items to read.")
@click.option("-c", "--category",
              help="The category of the items to read.")
@click.option("-v", "--value",
              help="The value of the items to read.")
def delete(id: str, name: str, category: str, value: float):
    changes = models.delete(id, name, category, value)
    print(f"Amount of rows deleted: {changes} rows")

@cli.command()
@click.argument("output")
@click.option("-t", "--type",
              default="CSV",
              help="The file type of the output.")
def export_db(output: str, type: str):
    changes = services.export_db(output, type)
    print(f"Amount of rows exported: {changes} rows")

@cli.command()
@click.argument("input")
@click.option("-t", "--type",
              default="CSV",
              help="The file type of the input.")
def import_db(input: str, type: str):
    changes = services.import_db(input, type)
    print(f"Amount of rows imported: {changes} rows")

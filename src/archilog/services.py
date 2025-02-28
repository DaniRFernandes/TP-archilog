import csv
import dataclasses
import io

import archilog.models as models


def export_db(output: str, type: str):
    items_table, total_changes = models.select(None, None, None, None)

    match type.upper():
        case "CSV":
            with open(output, "w", newline="") as f:
                writer = csv.writer(f)

                for row in items_table:
                    writer.writerow(row)
        case _:
            print("This type output has not been implemented yet.")

    return total_changes

def import_db(input: str, type: str):
    nb_inserted_lines = 0

    match type.upper():
        case "CSV":
            with open(input, "r", newline="") as f:
                reader = csv.reader(f)

                for row in reader:
                    models.insert(str(row[0]), row[1], row[2], row[3])
                    nb_inserted_lines += 1
        case _:
            print("This type output has not been implemented yet.")

    return nb_inserted_lines

def export_web():
    output = io.StringIO()

    csv_writer = csv.DictWriter(output, fieldnames=[f.name for f in dataclasses.fields(models.Item)])
    csv_writer.writeheader()

    items_table = models.select()

    for item in items_table:
        csv_writer.writerow({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "value": item.value
        })

    output.seek(0)

    return output

def import_web(input_stream):
    csv_reader = csv.reader(input_stream.read().decode("utf-8").splitlines())
    header = next(csv_reader)

    for row in csv_reader:
        id, name, category, value = row
        amount = float(amount)

        models.insert(id, name, category, value)

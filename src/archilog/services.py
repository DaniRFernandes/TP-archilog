import csv

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

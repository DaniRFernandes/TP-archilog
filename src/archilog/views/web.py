import os

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from unearth.fetchers import Response

import archilog.models as models
import archilog.services as services


app = Flask(__name__)

@app.route("/select/")
@app.route("/select/", methods=["POST"])
@app.route("/select/<delete_id>")
@app.route("/select/<delete_id>", methods=["POST"])
def select_page(delete_id=None):
    name, category, value = None, None, None

    if delete_id:
        models.delete(delete_id, None, None, None)

    if "input-name" in request.form:
        name = request.form["input-name"]
    if "input-category" in request.form:
        category = request.form["input-category"]
    if "input-value" in request.form:
        value = request.form["input-value"]

    items_table, nb_selected_rows = models.select(None, name, category, value)

    return render_template("select.html",
                           items_table=items_table,
                           nb_selected_rows=nb_selected_rows)

@app.route("/create/")
@app.route("/create/", methods=["POST"])
def create_page():
    if "name" in request.form and "value" in request.form:
        name = request.form["name"]
        value = request.form["value"]

        if len(name) > 0 and len(value) > 0:
            if "category" in request.form:
                category = request.form["category"]
                models.insert(None, name, category, value)
            else:
                models.insert(None, name, None, value)

    return render_template("create.html")

@app.route("/update/<update_id>")
@app.route("/update/<update_id>", methods=["POST"])
def update_page(update_id=None):
    if not update_id:
        return redirect(url_for("select_page"))

    name, category, value = None, None, None

    if "name" not in request.form:
        return render_template("update.html")

    if len(request.form["name"]) > 0:
        name = request.form["name"]

    if len(request.form["category"]) > 0:
        category = request.form["category"]

    if len(request.form["value"]) > 0:
        value = request.form["value"]

    models.update(update_id, None, None, None, name, category, value)

    return redirect(url_for("select_page"))

@app.route("/csv/")
@app.route("/csv/", methods=["POST"])
def csv_page():
    if "csv-import" in request.form:
        csv_import = request.files["csv-import"]
        services.import_web(csv_import.stream, "CSV")

        return redirect(url_for("select_page"))
    elif "export-submit" in request.form:
        output = services.export_web()

        response = Response(output.getvalue(), mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=entries.csv"

        return response

    return render_template("csv.html")

from flask import request, render_template, redirect, url_for, Response, Blueprint, flash

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange

import archilog.models as models
import archilog.services as services


class ItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category")
    value = DecimalField("Value", validators=[DataRequired(), NumberRange(min=0)])

web_ui = Blueprint("web_ui", __name__, url_prefix="/")

@web_ui.route("/<page>")
def show(page):
    return render_template(f"templates/{page}.html")

@web_ui.route("/submit", methods=["GET", "POST"])
def submit():
    form = ItemForm()

    if form.validate_on_submit():
        return redirect("/success")

    return render_template("submit.html", form=form)

@web_ui.errorhandler(500)
def handle_internal_error(error):
    flash("Erreur interne du serveur", "error")

    return redirect(url_for("web_ui.index_page"))

@web_ui.route("/")
def index_page():
    models.init_db()

    return redirect(url_for("web_ui.select_page"))

@web_ui.route("/select/")
@web_ui.route("/select/", methods=["POST"])
@web_ui.route("/select/<delete_id>")
@web_ui.route("/select/<delete_id>", methods=["POST"])
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

@web_ui.route("/create/")
@web_ui.route("/create/", methods=["POST"])
def create_page():
    form = ItemForm()

    if "name" in request.form and "value" in request.form:
        name = request.form["name"]
        value = request.form["value"]

        if len(name) > 0 and len(value) > 0:
            if "category" in request.form:
                category = request.form["category"]
                models.insert(None, name, category, value)
            else:
                models.insert(None, name, None, value)

            return redirect(url_for("web_ui.select_page"))

    return render_template("create.html", form=form)

@web_ui.route("/update/<update_id>")
@web_ui.route("/update/<update_id>", methods=["POST"])
def update_page(update_id=None):
    if not update_id:
        return redirect(url_for("web_ui.select_page"))

    item = models.select(update_id, None, None, None)[0][0]

    form = ItemForm(name=item[1], category=item[2], value=item[3])

    name, category, value = None, None, None

    if "name" not in request.form:
        return render_template("update.html", form=form)

    if len(request.form["name"]) > 0:
        name = request.form["name"]

    if len(request.form["category"]) > 0:
        category = request.form["category"]

    if len(request.form["value"]) > 0:
        value = request.form["value"]

    models.update(update_id, None, None, None, name, category, value)

    return redirect(url_for("web_ui.select_page"))

@web_ui.route("/csv/")
@web_ui.route("/csv/", methods=["POST"])
def csv_page():
    if "csv-import" in request.files:
        csv_import = request.files["csv-import"]
        services.import_web(csv_import)

        return redirect(url_for("web_ui.select_page"))
    elif "export-submit" in request.form:
        output = services.export_web()

        response = Response(output.getvalue(), mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=entries.csv"

        return response

    return render_template("csv.html")

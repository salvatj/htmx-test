from py4web import action, request, abort, redirect, URL, Field, DAL
from yatl.helpers import A, BUTTON, INPUT
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form, FormStyleBulma, FormStyleDefault, RadioWidget
from py4web.utils.grid import Grid, Column, GridClassStyle, GridClassStyleBulma
import datetime

@action("index")
@action.uses("index.html")
def index():
    return dict(message="Hello")

@action("simple_form", method=["GET", "POST"])
@action("simple_form/<id>", method=["GET", "POST"])
@action.uses("simple_form.html", session, db)
def simple_form(id=None):
    form = Form(db.person, id, deletable=False, formstyle=FormStyleDefault)
    rows = db(db.person).select()
    return dict(form=form, rows=rows, timestamp=datetime.datetime.now())

@action("simple_grid", method=["GET", "POST"])
@action.uses( "simple_grid.html", session, db)
def simple_grid():
    fields = [
        db.person.name,
        db.person.job,
    ]
    grid = Grid(db.person, fields=fields)
    return dict(grid=grid, timestamp=datetime.datetime.now())

@action("htmx_form_demo")
@action.uses("htmx_form_demo.html")
def htmx_form_demo():
    return dict(timestamp=datetime.datetime.now())

@action("htmx_list", method=["GET", "POST"])
@action.uses("htmx_list.html", db)
def htmx_list():
    persons = db(db.person.id > 0).select()
    return dict(persons=persons)

@action("htmx_form/<record_id>", method=["GET", "POST"])
@action.uses("htmx_form.html", db)
def htmx_form(record_id=None):
    attrs = {
        "_hx-post": URL("htmx_form/%s" % record_id),
        "_hx-target": "#htmx-form-demo",
    }
    form = Form(db.person, record=db.person(record_id), **attrs)
    if form.accepted:
        redirect(URL("htmx_list"))
    cancel_attrs = {
        "_hx-get": URL("htmx_list"),
        "_hx-target": "#htmx-form-demo",
    }
    form.param.sidecar.append(A("Cancel", **cancel_attrs))
    return dict(form=form)

@action("htmx_grid_demo")
@action.uses("htmx_grid_demo.html")
def htmx_grid_demo():
    return dict(timestamp=datetime.datetime.now())

@action("htmx_grid", method=["GET", "POST"])
@action.uses( "htmx_grid.html", session, db)
def htmx_grid():
    fields = [
        db.person.name,
        db.person.job,
    ]
    grid = Grid(db.person, fields=fields, auto_process=False)
    attrs = {
        "_hx-get": URL("htmx_grid"),
        "_hx-target": "#htmx-grid-demo",
    }
    grid.process()
    return dict(grid=grid)

#------------------------------------------

@action("htmx_demo")
@action.uses("htmx_demo.html")
def htmx_demo():
    return dict(timestamp=datetime.datetime.now())

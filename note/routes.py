import datetime
import uuid
from dataclasses import asdict

from flask import (Blueprint, abort, current_app, redirect, render_template,
                   request, url_for)

from note.models import Note

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    notes_data = current_app.db.note.find({})
    notes = [Note(**note) for note in notes_data]
    return render_template("index.html", title="Notes", notes=notes)

@pages.route("/add", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        note = Note(
            _id = uuid.uuid4().hex,
            title = request.form.get("title"),
            date = datetime.datetime.today(),
            content = request.form.get("content")
        )
        current_app.db.note.insert_one(asdict(note))
        
        return redirect(url_for(".index"))
    
    return render_template("new_note.html", title="Notes | add note")

@pages.get("/note/<string:_id>")
def note(_id: str):
    note_data = current_app.db.note.find_one({'_id': _id})
    if not note_data:
        abort(404)
    note = Note(**note_data)
    return render_template("note_details.html", note=note)


@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
def edit_note(_id: str):
    note_data = current_app.db.note.find_one({'_id': _id})
    if not note_data:
        abort(404)
    note = Note(**note_data)
    
    if request.method == "POST":
        note.title = request.form.get("title")
        note.date = datetime.datetime.today()
        note.content = request.form.get("content")
        
        current_app.db.note.update_one({'_id': _id}, {'$set': asdict(note)})
        
        return redirect(url_for(".note", _id=_id))
    
    return render_template("new_note.html", note=note)
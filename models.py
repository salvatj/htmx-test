from . import settings
from .common import db, Field, T
from pydal.validators import *
from py4web import URL

db.define_table(
    "person",
    Field("name", requires=IS_NOT_IN_DB(db, "person.name"), label=T("name")),
    Field("job", requires=IS_NOT_EMPTY(), label=T("job")),
    Field("foto", "upload", autodelete=True, 
          uploadfolder=settings.UPLOAD_FOLDER,
          download_url=lambda v: URL("static/uploads", v) if v else ""),
    format="%(name)s",
)

if not db(db.person).count():
    db.person.insert(name="Clark Kent", job="Journalist")
    db.person.insert(name="Peter Park", job="Photographer")
    db.person.insert(name="Bruce Wayne", job="CEO")

db.commit()

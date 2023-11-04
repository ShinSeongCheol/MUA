from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

from mua.models import *

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def main():
    return render_template("main/main.html")

from flask import Blueprint

groups_bp = Blueprint("groups", __name__)

@groups_bp.route("/", methods=["GET"])
def get_groups():
    return {"message": "List of groups"}
from model.user_model import user_model
from flask import Blueprint, request, send_file
from datetime import datetime
from model.auth_model import auth_model

user_blueprint = Blueprint('user', __name__)
# DB Object
obj = user_model()
auth = auth_model()

@user_blueprint.route("/user/getall")
@auth.token_auth()
def user_getall():
    return obj.user_getall_model()

@user_blueprint.route("/user/addnew", methods=["POST"])
def user_addnew():
    return obj.user_addnew_model(request.form)

@user_blueprint.route("/user/update", methods=["PUT"])
def user_update():
    return obj.user_update_model(request.form)

@user_blueprint.route("/user/delete/<id>", methods=["DELETE"])
def user_delete(id):
    return obj.user_delete_model(id)

@user_blueprint.route("/user/patch/<id>", methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)

@user_blueprint.route("/user/getall/limit/<limit>/page/<page>", methods=["GET"])
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)

@user_blueprint.route("/user/<uid>/upload/avatar", methods=["PUT"])
def user_upload_avatar(uid):
    file = request.files['avatar']

    uniqueFileName = str(datetime.now().timestamp()).replace(".", "")
    fileNameSplit = file.filename.split(".")
    ext = fileNameSplit[len(fileNameSplit)-1]
    file.save(f"Uploads/Images/Users/{uniqueFileName}.{ext}")
    finalFilePath = f"Uploads/Images/Users/{uniqueFileName}.{ext}"
    return obj.user_upload_avatar_model(uid, finalFilePath)

@user_blueprint.route("/uploads/<filename>")
def user_getavatar_controller(filename):
    return send_file(f"uploads/Images/Users/{filename}")

@user_blueprint.route("/user/login", methods=["POST"])
def user_login_controller():

    return obj.user_login_model(request.form)


@user_blueprint.route("/user/addmultiple", methods=["POST"])
def user_addmultiple_controller():
    return obj.user_addmultiple_model(request.json)
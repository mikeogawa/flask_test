from flask import Flask, render_template, request, session, redirect, url_for
from models.models import FoodDB, User
from models.database import db_session
from datetime import datetime
from app import key
from hashlib import sha256

app = Flask(__name__)
app.secret_key = key.SECRET_KEY

def fix_date(exp):
    if "/" in exp:
        return datetime.strptime(exp,"%Y/%m/%d")
    elif "-" in exp:
        return datetime.strptime(exp,"%Y-%m-%d")
    else:
        pass

def assertError(title,desc,exp):
    if title == "":
        return "No Blanks Allowed"
    if exp is None:
        return "recheck data"
    else:
        return None


@app.route("/")
@app.route("/index")
def index():
    if "user_name" not in session:
        return redirect(url_for("top",status="logout"))
    title = request.args.get("title")
    foods = FoodDB.query.all()
    return render_template("index.html",
                            title=title,
                            foods=foods,
                            current_edit=None,
                            error_msg=None)

def errorMode(msg):
    title = request.args.get("title")
    foods = FoodDB.query.all()
    return render_template("index.html",
                            title=title,
                            foods=foods,
                            current_edit=None,
                            error_msg=msg)

def editMode(title,foods,content):
    return render_template("index.html",
                            title=title,
                            foods=foods,
                            current_edit=content,
                            error_msg=None)


@app.route("/index", methods=["post"])
def post():
    if request.form["btn"] == "Add":
        title = request.form["title"]
        desc = request.form["desc"]
        exp = request.form["exp"]
        exp = fix_date(exp)
        msg = assertError(title,desc,exp)
        if msg:
            return errorMode(msg)

        content = FoodDB(title,desc,exp)
        db_session.add(content)
        db_session.commit()

    if request.form["btn"] == "Edit":
        idx = request.form["idx"]
        title = request.form["title"]
        desc = request.form["desc"]
        exp = request.form["exp"]
        exp = fix_date(exp)

        msg = assertError(title,desc,exp)
        if msg:
            return errorMode(msg)

        content = FoodDB.query.filter_by(id=idx).first()
        content.title = title
        content.body = desc
        content.expire = exp
        content.date = datetime.now()
        db_session.commit()

    if request.form["btn"] == "Delete":
        id_list = request.form.getlist("delete")
        for idx in id_list:
            content = FoodDB.query.filter_by(id=idx).first()
            db_session.delete(content)
        db_session.commit()

    return index()

@app.route("/edit")
def edit():
    idx = request.args.get("id")
    title = request.args.get("title")
    foods = FoodDB.query.all()
    content = FoodDB.query.filter_by(id=idx).first()
    return editMode(title,foods,content)


@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    desc = request.form["desc"]
    exp = request.form["exp"]

    if "/" in exp:
        exp = datetime.strptime(exp,"%Y/%m/%d")
    elif "-" in exp:
        exp = datetime.strptime(exp,"%Y-%m-%d")
    else:
        pass
    content = FoodDB(title,desc,exp)
    db_session.add(content)
    db_session.commit()
    return index()

@app.route("/login",methods=["post"])
def login():
    user_name = request.form["user"]
    user = User.query.filter_by(user=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))

@app.route("/register",methods=["post"])
def register():
    user_name = request.form["user"]
    user = User.query.filter_by(user=user_name).first()
    if user:
        return redirect(url_for("new",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)

@app.route("/register")
def newcomer():
    status = request.args.get("status")
    return render_template("new.html",status=status)

if __name__ == "__main__":
    app.run(debug=True)

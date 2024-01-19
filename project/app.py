import os

from cs50 import SQL
from flask import Flask, redirect, render_template, flash, request, url_for

# Configure application
app = Flask(__name__)

# Configure session to use secret key
app.config["SECRET_KEY"] = 'DgCoE9Qbqv1WQNPK8gtD'

# Configure SQLite3
fooddb = SQL("sqlite:///food.db")
recipedb = SQL("sqlite:///recipes.db")


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/calories")
def calories():

    return render_template("calories.html")


@app.route("/HBcalories", methods=["GET", "POST"])
def HBcalories():
    # User reached route via POST
    if request.method == "POST":

        # Get user entered gender
        hbgender = request.form.get("hbgender")

        # Get user entered weight
        hbweight = float(request.form.get("hbweight"))

        # Get user entered height
        hbheight = float(request.form.get("hbheight"))

        # Get user entered age
        hbage = int(request.form.get("hbage"))

        # Get user entered activity level
        hbactlvl = float(request.form.get("hbactivity-lvl"))

        # Calcuates HB equation to return to user if user is male
        if hbgender == "male":
            userhbres = (66.47 + (13.75 * hbweight) + (5.003 * hbheight) - (6.755 * hbage)) * hbactlvl
            userhbres = int(userhbres)
            flash(f"Your recommended amount of calories is {userhbres}kcals")
        #Calcuates HB equation to return to user is female
        else:
            userhbres = (655.1 + (9.563 * hbweight) + (1.850 * hbheight) - (4.676 * hbage)) * hbactlvl
            userhbres = int(userhbres)
            flash(f"Your recommended amount of calories is {userhbres}kcals")

    return render_template("HBcalories.html")


@app.route("/MSJcalories", methods=["GET", "POST"])
def MSJcalories():
    # User reached route via POST
    if request.method == "POST":

        # Get user entered gender
        msjgender = request.form.get("msjgender")

        # Get user entered weight
        msjweight = float(request.form.get("msjweight"))

        # Get user entered height
        msjheight = float(request.form.get("msjheight"))

        # Get user entered age
        msjage = int(request.form.get("msjage"))

        # Get user entered activity level
        msjactlvl = float(request.form.get("msjactivity-lvl"))

        # Calcuates HB equation to return to user if user is male
        if msjgender == "male":
            usermsjres = (5 + (10 * msjweight) + (6.25 * msjheight) - (5 * msjage)) * msjactlvl
            usermsjres = int(usermsjres)
            flash(f"Your recommended amount of calories is {usermsjres}kcals")
        # Calcuates HB equation to return to user if user is female
        else:
            usermsjres = (161 - (10 * msjweight) + (6.25 * msjheight) - (5 * msjage)) * msjactlvl
            usermsjres = int(usermsjres)
            flash(f"Your recommended amount of calories is {usermsjres}kcals")

    return render_template("MSJcalories.html")


@app.route("/water", methods=["POST", "GET"])
def water():
    # User reached route via POST
    if request.method == "POST":

        # Get user entered weight
        waterweight = float(request.form.get("waterweight"))

        # Get user entered amout of physical activity
        waterphys = int(request.form.get("waterphys"))

        # Calculate min water intake using users values
        watermin = (waterweight * 40) + (waterphys * 800)
        watermin = int(watermin)

        # Calculate max water intake using user values
        watermax = (waterweight * 50) + (waterphys * 1000)
        watermax = int(watermax)

        # Display users max and min water intake in pop up message
        flash(f"Your daily water intake should be between {watermin}ml and {watermax}ml")

    return render_template("water.html")


@app.route("/recipes")
def recipes():
    # Query recipe db
    recipes = recipedb.execute(
        "SELECT * FROM recipes"
    )

    return render_template("recipes.html", recipes=recipes)


@app.route("/submit", methods=["GET", "POST"])
def submitrecipe():
    if request.method == "POST":
        # Get name of recipe from user form
        recname = request.form.get("recname")

        # Get calories of recipe from user form
        reccalories = float(request.form.get("calforone"))

        # Get protein of recipe from user form
        recprotein = float(request.form.get("protein"))

        # Get carbs of recipe from user form
        reccarbs = float(request.form.get("carbs"))

        # Get fats of recipe from user form
        recfat = float(request.form.get("fat"))

        # Get instructs of recipe from user form
        recinstructs = request.form.get("instructs")

        # Add receipe to database
        recipedb.execute(
            "INSERT INTO recipes (name, calories, protein, carbs, fats, instructs) VALUES (?, ?, ?, ?, ?, ?)",
            recname,
            reccalories,
            recprotein,
            reccarbs,
            recfat,
            recinstructs
        )
        return redirect("/")
    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("submit.html")


@app.route("/food", methods=["GET", "POST"])
def food():
    # Get search query if query is blank
    searchf = request.form.get("search-food")
    if searchf is None or (str(searchf).strip() == ""):
        food = fooddb.execute(
            "SELECT * FROM food"
        )
    # Get search query if query is populated
    else:
        food = fooddb.execute(
            "SELECT * FROM food WHERE name LIKE ?",
            searchf
        )
    return render_template("food.html", food=food, searchf=searchf)

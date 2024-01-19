import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user's stocks and shares

    # Get user session id
    user_id_session = session["user_id"]

    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id_session,
    )

    # Get user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id_session)[0]["cash"]

    # Initate variables
    total_value = cash
    grand_total = cash

    # Check table for user's stocks and shares
    for stock in stocks:
        # Get quote for symbol
        quote = lookup(stock["symbol"])

        # Initialize variables
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        stock["value"] = stock["value"]
        total_value += stock["value"]
        grand_total += stock["value"]

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template(
        "index.html",
        stocks=stocks,
        cash=cash,
        total_value=total_value,
        grand_total=grand_total,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user session id
        user_id_session = session["user_id"]

        # Convert symbol user entered to upper case
        symbol = request.form.get("symbol").upper()

        # Gets number of shares that user entered
        shares = request.form.get("shares")

        # Get quote for symbol
        quote = lookup(symbol)

        # Checking to see if user has entered a stock symbol
        if not symbol:
            return apology("enter a stock symbol")

        # Checking for a vaild number of shares
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("provide a number of shares")

        # Check to see if a valid symbol has been entered
        if quote is None:
            return apology("enter a valid stock symbol")

        # Check stock price
        price = quote["price"]

        # Calculates the total cost for the amount of shares
        total_cost = int(shares) * price

        # Get the amount of cash the user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id_session)[0][
            "cash"
        ]

        # Check if user has enough money to buy shares
        if cash < total_cost:
            return apology("not enough money")

        else:
            cash_now = cash - total_cost

            # Update users table
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", cash_now, user_id_session
            )

            # Add the transaction to the history table
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                user_id_session,
                symbol,
                shares,
                price,
            )

            # Display the transaction
            flash(f"Purchased {shares} shares of {symbol} for {usd(total_cost)}!")
            return redirect("/")

    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get user session id
    user_id_session = session["user_id"]

    # Query db
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        user_id_session,
    )

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get symbol that user entered
        symbol = request.form.get("symbol")

        # Lookup symbol user entered
        quote = lookup(symbol)

        # Check to see if symbol user entered is valid
        if not quote:
            return apology("invalid symbol", 400)

        # Return user to quote
        return render_template("quote.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Log out user if logged in
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was entered
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Check username doesn't already exist
        if len(rows) != 0:
            return apology("username is taken", 400)

        # Insert user into database
        rows = db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        # Check if user was inserted in to database
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Log user in
        session["user_id"] = rows[0]["id"]

        # Return user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get user session id
    user_id_session = session["user_id"]

    # Get the user's stock
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id_session,
    )

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Convert symbol user entered to upper case
        symbol = request.form.get("symbol").upper()

        # Gets number of shares that user entered
        shares = request.form.get("shares")

        # Checking to see if user has entered a stock symbol
        if not symbol:
            return apology("enter a stock symbol")

        # Checking for a vaild number of shares
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("provide a number of shares")

        # Convert shares from db to integer
        else:
            shares = int(shares)
            f_shares = int(shares)

        # Loop over stocks
        for stock in stocks:
            # Checking if user entered symbol matches symbol in db
            if stock["symbol"] == symbol:
                # Checking to see if user's
                if stock["total_shares"] < shares:
                    return apology("not enough shares")

                # Get quote for symbol
                else:
                    quote = lookup(symbol)

                    # Check to see if a valid symbol has been entered
                    if quote is None:
                        return apology("symbol not found")

                    # Check stock price
                    price = quote["price"]

                    # Calculates the total cost for the amount of shares
                    total_sale = shares * price
                    f_total_sale = total_sale

                    # Convert to negative numbers
                    total_sale = total_sale * -1
                    shares = shares * -1
                    price = price * -1

                    # Update users table
                    db.execute(
                        "UPDATE users SET cash = cash - ? WHERE id = ?",
                        total_sale,
                        user_id_session,
                    )

                    # Add the transaction to the history table
                    db.execute(
                        "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                        user_id_session,
                        symbol,
                        shares,
                        price,
                    )

                    # Display notification of transaction
                    flash(f"Sold {f_shares} shares of {symbol} for {usd(f_total_sale)}")
                    return redirect("/")

            return apology("symbol not found")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change user's password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user session id
        user_id_session = session["user_id"]

        # Query database for current password
        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id_session)

        # Ensure current password was entered
        if not request.form.get("password"):
            return apology("must provide current password", 400)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide new passwords again", 400)

        # Ensure passwords match
        elif request.form.get("new_password") != request.form.get("confirmation"):
            return apology("new passwords must match", 400)

        # Ensure current passwords is correct
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("current password incorrect", 400)

        # Ensure passwords match
        elif request.form.get("new_password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Insert new password into database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(request.form.get("new_password")),
            user_id_session,
        )

        # Return user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")

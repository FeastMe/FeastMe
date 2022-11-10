# CS340 Fall 2022
# Group 17 (FeastMe)
# Bianca Davies
# Elliott Larsen

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_larsenel'
app.config['MYSQL_PASSWORD'] = '9170' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_larsenel'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
# Welcome page.
@app.route('/')
def index():
    return render_template('index.j2')

# CRUD on accounts entity.
@app.route('/accounts', methods=['POST', 'GET'])
def accounts():
    # READ accounts
    if request.method == 'GET':
        query = "SELECT * FROM accounts;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        accounts = cur.fetchall()

        return render_template('accounts.j2', accounts = accounts)

@app.route('/edit_account/<int:account_id>', methods=['POST', 'GET'])
def edit_accounts(account_id):
    # UPDATE accounts
    if request.method == 'GET':
        query = "SELECT * FROM accounts WHERE account_id = %s" % (account_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
    
        return render_template('edit_account.j2', account = result)
    
    if request.method == 'POST':
        if request.form.get('Edit_Account'):
            account_id = request.form["account_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            phone_number = request.form["phone_number"]
            account_type = request.form["account_type"]

            query = "UPDATE accounts SET accounts.first_name = %s, accounts.last_name = %s, accounts.email = %s, accounts.password = %s, accounts.phone_number = %s, accounts.type = %s WHERE accounts.account_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, email, password, phone_number, account_type, account_id))
            mysql.connection.commit()

            return redirect('/accounts')

@app.route('/delete_account/<int:account_id>')
def delete_account(account_id):
    # DELETE accounts
    query = f"DELETE FROM accounts WHERE account_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (account_id,))
    mysql.connection.commit()

    return redirect('/accounts')

@app.route('/add_account')
def add_account():
    # CREATE account
    return "Add account"

@app.route('/patrons')
def patrons():
    return render_template('patrons.j2')

@app.route('/drivers')
def drivers():
        return render_template('drivers.j2')

@app.route('/chefs')
def chefs():
        return render_template('chefs.j2')

@app.route('/orders')
def orders():
        return render_template('orders.j2')

@app.route('/foods')
def foods():
        return render_template('foods.j2')

@app.route('/foodsingredients')
def foods_has_ingredients():
        return render_template('food-ingredients.j2')

@app.route('/ingredients')
def ingredients():
        return render_template('ingredients.j2')

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8081, debug=True)
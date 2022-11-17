# CS340 Fall 2022
# Group 17 (FeastMe)
# Bianca Davies
# Elliott Larsen

# Citation for the following functions:
# Date: 11/10/2022
# Copied from: CS340 Flask starter example code
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py 

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
###########################
# CRUD on accounts entity.#
###########################
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
def edit_account(account_id):
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
    try:
        query = f"DELETE FROM accounts WHERE account_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (account_id,))
        mysql.connection.commit()
        return redirect('/accounts')

    except:
        return "<h3>Not all entities have been implemented yet and you are trying to delete an account that is bound by foreign key constraints.</h3>"

@app.route('/add_account/', methods=['POST'])
def add_account():
    # CREATE account
    if request.method == 'POST':
        if request.form.get("Add_Account"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            phone_number = request.form["phone_number"]
            account_type = request.form["account_type"]

            query = "INSERT INTO accounts(first_name, last_name, email, password, phone_number, type) VALUES (%s, %s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, email, password, phone_number, account_type))
            mysql.connection.commit()

            return redirect('/accounts')

##########################
# CRUD on patrons entity.#
##########################
@app.route('/patrons', methods=['POST', 'GET'])
def patrons():
    # READ patrons
    if request.method == 'GET':
        query = "SELECT patrons.account_id, CONCAT(first_name, ' ', last_name) AS patron_name, street_number, street, unit_number, city, state, zip_code FROM accounts\
        INNER JOIN patrons ON patrons.account_id = accounts.account_id\
        ORDER by patrons.patron_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        patrons = cur.fetchall()

        query = "SELECT * FROM accounts WHERE accounts.type = 'Patron' AND accounts.account_id NOT IN (SELECT account_id FROM patrons);"
        cur = mysql.connection.cursor()
        cur.execute(query)
        unassigned_patrons = cur.fetchall()
        
        return render_template('patrons.j2', patrons = patrons, unassigned_patrons = unassigned_patrons)

@app.route('/edit_patron/<int:account_id>', methods=['POST', 'GET'])
def edit_patron(account_id):
    # UPDATE patron
    if request.method == 'GET':
        query = "SELECT patrons.account_id, CONCAT(first_name, ' ', last_name) AS patron_name, street_number, street, unit_number, city, state, zip_code FROM accounts\
        INNER JOIN patrons ON patrons.account_id = accounts.account_id\
        WHERE patrons.account_id = %s" % (account_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        patron = cur.fetchall()
    
        return render_template('edit_patron.j2', patron = patron)
    
    if request.method == 'POST':
        if request.form.get('Edit_Patron'):
            account_id = request.form["patron_id"]
            street_number = request.form["street_number"]
            street = request.form["street"]
            unit_number = request.form["unit_number"]
            city = request.form["city"]
            state = request.form["state"]
            zip_code = request.form["zip_code"]

            query = "UPDATE patrons SET patrons.street_number = %s, patrons.street = %s, patrons.unit_number = %s, patrons.city = %s, patrons.state = %s, patrons.zip_code = %s WHERE patrons.account_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (street_number, street, unit_number, city, state, zip_code, account_id))
            mysql.connection.commit()

            return redirect('/patrons')

@app.route('/delete_patron/<int:account_id>')
def delete_patron(account_id):
    # DELETE patron
    query = f"DELETE FROM patrons WHERE account_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (account_id,))
    mysql.connection.commit()
    return redirect('/patrons')


@app.route('/add_patron/', methods=['POST'])
def add_patron():
    # CREATE patron
    if request.method == "POST":
        if request.form.get("Add_Patron"):
            account_id = request.form['patron_id']
            street_number = request.form['street_number']
            street = request.form['street']
            unit_number = request.form['unit_number']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']

            query2 = "INSERT INTO patrons(account_id, street_number, street, unit_number, city, state, zip_code) VALUES(%s, %s, %s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query2, (account_id, street_number, street, unit_number, city, state, zip_code))
            mysql.connection.commit()

            return redirect('/patrons')

##########################
# CRUD on drivers entity.#
##########################
@app.route('/drivers', methods=['POST', 'GET'])
def drivers():
    # READ drivers
    if request.method == 'GET':
        query = "SELECT drivers.account_id, CONCAT(first_name, ' ', last_name) AS driver_name, license_plate, license_number FROM accounts\
        INNER JOIN drivers ON drivers.account_id = accounts.account_id\
        ORDER BY drivers.driver_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        drivers = cur.fetchall()

        query = "SELECT * FROM accounts WHERE accounts.type = 'Driver' AND accounts.account_id NOT IN (SELECT account_id FROM drivers);"
        cur = mysql.connection.cursor()
        cur.execute(query)
        unassigned_drivers = cur.fetchall()

        return render_template('drivers.j2', drivers = drivers, unassigned_drivers = unassigned_drivers)

@app.route('/edit_driver/<int:account_id>', methods=['POST', 'GET'])
def edit_driver(account_id):
    # UPDATE driver
    if request.method == 'GET':
        query = "SELECT drivers.account_id, CONCAT(first_name, ' ', last_name) AS driver_name, license_plate, license_number FROM accounts\
        INNER JOIN drivers ON drivers.account_id = accounts.account_id\
        WHERE drivers.account_id = %s" % (account_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        driver = cur.fetchall()
    
        return render_template('edit_driver.j2', driver = driver)
    
    if request.method == 'POST':
        if request.form.get('Edit_Driver'):
            account_id = request.form["driver_id"]
            license_plate = request.form["license_plate"]
            license_number = request.form["license_number"]

            query = "UPDATE drivers SET drivers.license_plate = %s, drivers.license_number = %s WHERE drivers.account_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (license_plate, license_number, account_id))
            mysql.connection.commit()

            return redirect('/drivers')

@app.route('/delete_driver/<int:account_id>')
def delete_driver(account_id):
    # DELETE driver
    query = f"DELETE FROM drivers WHERE account_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (account_id,))
    mysql.connection.commit()
    return redirect('/drivers')

@app.route('/add_driver/', methods=['POST'])
def add_driver():
    # CREATE driver
    if request.method == "POST":
        if request.form.get("Add_Driver"):
            account_id = request.form['driver_id']
            license_plate = request.form['license_plate']
            license_number = request.form['license_number']

            query = "INSERT INTO drivers(account_id, license_plate, license_number) VALUES(%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (account_id, license_plate, license_number))
            mysql.connection.commit()

            return redirect('/drivers')

########################
# CRUD on chefs entity.#
########################
@app.route('/chefs', methods=['POST', 'GET'])
def chefs():
    # READ chefs
    if request.method == 'GET':
        query = "SELECT chefs.account_id, CONCAT(first_name, ' ', last_name) AS chef_name, cert_number, specialty, type FROM accounts\
        INNER JOIN chefs ON chefs.account_id = accounts.account_id\
        ORDER BY chefs.chef_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        chefs = cur.fetchall()

        query = "SELECT * FROM accounts WHERE accounts.type = 'Chef' AND accounts.account_id NOT IN (SELECT account_id FROM chefs);"
        cur = mysql.connection.cursor()
        cur.execute(query)
        unassigned_chefs = cur.fetchall()

        return render_template('chefs.j2', chefs = chefs, unassigned_chefs = unassigned_chefs)

@app.route('/edit_chef/<int:account_id>', methods=['POST', 'GET'])
def edit_chef(account_id):
    # UPDATE chef
    if request.method == 'GET':
        query = "SELECT chefs.account_id, CONCAT(first_name, ' ', last_name) AS chef_name, cert_number, specialty, type FROM accounts\
        INNER JOIN chefs ON chefs.account_id = accounts.account_id\
        WHERE chefs.account_id = %s" % (account_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        chef = cur.fetchall()
    
        return render_template('edit_chef.j2', chef = chef)
    
    if request.method == 'POST':
        if request.form.get('Edit_Chef'):
            account_id = request.form["chef_id"]
            cert_number = request.form["cert_number"]
            specialty = request.form["specialty"]

            query = "UPDATE chefs SET chefs.cert_number = %s, chefs.specialty = %s WHERE chefs.account_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (cert_number, specialty, account_id))
            mysql.connection.commit()

            return redirect('/chefs')

@app.route('/delete_chef/<int:account_id>')
def delete_chef(account_id):
    # DELETE chef
    query = f"DELETE FROM chefs WHERE account_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (account_id,))
    mysql.connection.commit()
    return redirect('/chefs')

@app.route('/add_chef/', methods=['POST'])
def add_chef():
    # CREATE chef
    if request.method == "POST":
        if request.form.get("Add_Chef"):
            account_id = request.form['chef_id']
            cert_number = request.form['cert_number']
            specialty = request.form['specialty']

            query = "INSERT INTO chefs(account_id, cert_number, specialty) VALUES(%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (account_id, cert_number, specialty))
            mysql.connection.commit()

            return redirect('/chefs')

##########################
# CRUD on orderss entity.#
##########################
@app.route('/orders', methods=['POST', 'GET'])
def orders():
    # READ orders
    if request.method == 'GET':
        query = "SELECT order_id, CONCAT(first_name, ' ', last_name) AS ordered_by, street_number, street, unit_number, city, state, zip_code, CONCAT(street_number, ' ', street, ' ', unit_number, ' ', city, ' ', state, ' ', zip_code) AS patron_address, license_plate, order_time, total_price, order_status\
        FROM orders\
        INNER JOIN accounts ON orders.ordered_by = accounts.account_id\
        INNER JOIN patrons ON orders.ordered_by = patrons.account_id\
        INNER JOIN drivers ON orders.delivery_by = drivers.account_id\
        ORDER BY order_time DESC;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        orders = cur.fetchall()

        return render_template('orders.j2', orders = orders)

@app.route('/edit_order/<int:order_id>', methods=['POST', 'GET'])
def edit_order(order_id):
    # UPDATE order
    pass

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    # DELETE order
    pass

@app.route('/add_order/', methods=['POST'])
def add_order():
    # CREATE order
    pass


########################
# CRUD on foods entity.#
########################
@app.route('/foods', methods=['POST', 'GET'])
def foods():
    # READ foods
    if request.method == 'GET':
        query = "SELECT * FROM foods;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        foods = cur.fetchall()

        return render_template('foods.j2', foods = foods)

@app.route('/edit_food/<int:food_id>', methods=['POST', 'GET'])
def edit_food(food_id):
    # UPDATE food
    if request.method == "GET":
        query = "SELECT * FROM foods WHERE food_id = %s" % (food_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return render_template('edit_food.j2', food = result)
    
    if request.method == "POST":
        if request.form.get("Edit_Food"):
            food_id = request.form["food_id"]
            order_id = request.form["order_id"]
            made_by = request.form["made_by"]
            food_name = request.form["food_name"]
            description = request.form["description"]
            is_vegan = request.form["is_vegan"]
            is_vegetarian = request.form["is_vegetarian"]
            price = request.form["price"]

            query = "UPDATE foods SET foods.order_id = %s, foods.made_by = %s, foods.food_name = %s, foods.description = %s, foods.is_vegan = %s, foods.is_vegetarian = %s, foods.price = %s WHERE foods.food_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id, made_by, food_name, description, is_vegan, is_vegetarian, price, food_id))
            mysql.connection.commit()

            return redirect('/foods')


@app.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    # DELETE food
    query = f"DELETE FROM foods WHERE food_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (food_id,))
    mysql.connection.commit()
    return redirect('/foods')

@app.route('/add_food/', methods=['POST'])
def add_food():
    # CREATE food
    pass

########################################
# CRUD on foods_has_ingredients entity.#
########################################
@app.route('/foodsingredients', methods=['POST', 'GET'])
def foods_has_ingredients():
    # READ foods_has_ingredients
    if request.method == 'GET':
        query = "SELECT f_has_i_id, foods.food_name, ingredients.ingredient_name FROM foods_has_ingredients\
        INNER JOIN foods ON foods_has_ingredients.food_id = foods.food_id\
        INNER JOIN ingredients ON foods_has_ingredients.ingredient_id = ingredients.ingredient_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        foods_ingredients = cur.fetchall()

        return render_template('food-ingredients.j2', foods_ingredients = foods_ingredients)

@app.route('/edit_foods_ingredients/<int:f_has_i_id>', methods=['POST', 'GET'])
def edit_foods_ingredients(f_has_i_id):
    # UPDATE foods_has_ingredients
    pass

@app.route('/delete_foods_ingredients/<int:f_has_i_id>')
def delete_foods_ingredients(f_has_i_id):
    # DELETE foods_has_ingredients
    pass

@app.route('/add_foods_ingredients/', methods=['POST'])
def add_foods_ingredients():
    # CREATE foods_has_ingredients
    pass

##############################
# CRUD on ingredients entity.#
##############################
@app.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    # READ ingredients
    if request.method == 'GET':
        query = "SELECT * FROM ingredients;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        ingredients = cur.fetchall()

        return render_template('ingredients.j2', ingredients = ingredients)

@app.route('/edit_ingredient/<int:ingredient_id>', methods=['POST', 'GET'])
def edit_ingredient(ingredient_id):
    # UPDATE ingredient
    if request.method == "GET":
        query = "SELECT * FROM ingredients WHERE ingredient_id = %s" % (ingredient_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return render_template('edit_ingredient.j2', ingredient = result)

    if request.method == "POST":
        if request.form.get('Edit_Ingredient'):
            ingredient_id = request.form['ingredient_id']
            ingredient_name = request.form['ingredient_name']
            expiry_date = request.form['expiry_date']
            in_stock = request.form['in_stock']

            query = "UPDATE ingredients SET ingredients.ingredient_name = %s, ingredients.expiry_date = %s, ingredients.in_stock = %s WHERE ingredients.ingredient_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (ingredient_name, expiry_date, in_stock, ingredient_id))
            mysql.connection.commit()

            return redirect('/ingredients')

@app.route('/delete_ingredient/<int:ingredient_id>')
def delete_ingredient(ingredient_id):
    # DELETE ingredient
    query = f"DELETE FROM ingredients WHERE ingredient_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (ingredient_id, ))
    mysql.connection.commit()

    return redirect('/ingredients')

@app.route('/add_ingredient/', methods=['POST'])
def add_ingredient():
    # CREATE ingredient
    pass



# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8080, debug=True)
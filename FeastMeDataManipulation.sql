------------
/* CREATE */
------------
-- Add a new account
INSERT INTO accounts(first_name, last_name, email, password, phone_number, type) VALUES (:first_name_input, :last_name_input, :email_input, :password_input, :phone_number_input, :type_from_dropdown_input)
-- Add a new patron (associate an account with patron attributes)
INSERT INTO patrons(account_id, street_number, street, unit_number, city, state, zip_code) VALUES (:account_id_FK, :street_number_input, :street_input, :unit_number_input, :city_input, :state_input, :zip_code_input)
-- Add a new driver (associate an account with driver attributes)
INSERT INTO drivers(account_id, license_plate, license_number) VALUES (:account_id_FK, :license_plate_input, :license_number_input)
-- Add a new chef (associate an account with chef attributes)
INSERT INTO chefs(account_id, cert_number, specialty) VALUES (:account_id_FK, :cert_number_input, :specialty_input)
-- Add a new order
INSERT INTO orders(ordered_by, delivery_by, order_time, total_price, order_status) VALUES (:ordered_by_FK, :delivery_by_FK, :order_time_input, :total_price_input, :order_status_input)
-- Add a new food
INSERT INTO foods(order_id, food_name, description, is_vegan, is_vegetarian, price) VALUES (:order_id_FK, :food_name_input, :description_input, :is_vegan_input, :is_vegetarian_input, :price_input)
-- Add a new ingredient
INSERT INTO ingredients(ingredient_name, expiry_date, in_stock) VALUES (:ingredient_name_input, :expiry_date_input, :in_stock_input)

----------
/* READ */
----------
-- Get all patrons with their full names
SELECT first_name, last_name, type FROM accounts
INNER JOIN patrons ON patrons.account_id = accounts.account_id
ORDER by patrons.account_id;
-- Get all drivers with their full names and license place.
SELECT first_name, last_name, license_plate, type FROM accounts
INNER JOIN drivers ON drivers.account_id = accounts.account_id
ORDER BY drivers.account_id;
-- Get all chefs with their full names, and specialties
SELECT first_name, last_name, specialty, type FROM accounts
INNER JOIN chefs ON chefs.account_id = accounts.account_id
ORDER BY chefs.account_id;
/************  WORKONTHIS  
-- Get all orders with patron's name, delivery driver's license plate, order time, total price, and order status
SELECT first_name, last_name, CONCAT(first_name, ' ', last_name) AS patron_name, license_plate, order_time, total_price, order_status FROM orders
INNER JOIN patrons ON patrons.account_id = orders.order_id
************/
-- Get all foods with their names, order_id, description, whether they are vegan or vegetariain, and price.
SELECT food_name, order_id, description, is_vegan, is_vegetarian, price FROM foods;
-- Get all ingredients with their name, expiry date, and whether they are in stock or not.
SELECT ingredient_name, expiry_date, in_stock FROM ingredients;

------------
/* UPDATE */
------------


------------
/* DELETE */
------------
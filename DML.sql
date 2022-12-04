------------
/* CREATE */
------------
-- Add a new account
INSERT INTO accounts(first_name, last_name, email, password, phone_number, type) VALUES (:first_name_input, :last_name_input, :email_input, :password_input, :phone_number_input, :type_from_dropdown_input);
-- Add a new patron (associate an account with patron attributes)
INSERT INTO patrons(account_id, street_number, street, unit_number, city, state, zip_code) VALUES (:account_id_FK, :street_number_input, :street_input, :unit_number_input, :city_input, :state_input, :zip_code_input);
-- Add a new driver (associate an account with driver attributes)
INSERT INTO drivers(account_id, license_plate, license_number) VALUES (:account_id_FK, :license_plate_input, :license_number_input);
-- Add a new chef (associate an account with chef attributes)
INSERT INTO chefs(account_id, cert_number, specialty) VALUES (:account_id_FK, :cert_number_input, :specialty_input);
-- Add a new order
INSERT INTO orders(ordered_by, delivery_by, order_time, total_price, order_status) VALUES (:ordered_by_FK, :delivery_by_FK, :order_time_input, :total_price_input, :order_status_input);
-- Add a new food
INSERT INTO foods(food_id, order_id, made_by, food_name, description, is_vegan, is_vegetarian, price) VALUES (:order_id_FK, :made_by_input, :food_name_input, :description_input, :is_vegan_input, :is_vegetarian_input, :price_input);
-- Add a new ingredient
INSERT INTO ingredients(ingredient_name, expiry_date, in_stock) VALUES (:ingredient_name_input, :expiry_date_input, :in_stock_input);
-- Add to the intersection table
INSERT INTO foods_has_ingredients(food_id, ingredient_id) VALUES (:food_id, :ingredient_id);

----------
/* READ */
----------
-- Get all attributes from accounts entity
SELECT * FROM accounts;
-- Search accounts entity by name
SELECT account_id, first_name, last_name, email, password, phone_number, type FROM accounts WHERE first_name = :first_name_input AND last_name = :last_name_input;
-- Get all patrons info
SELECT patrons.account_id, CONCAT(first_name, ' ', last_name) AS patron_name, street_number, street, unit_number, city, state, zip_code FROM accounts
INNER JOIN patrons ON patrons.account_id = accounts.account_id
ORDER by patrons.account_id;
-- Search patrons entity by patron ID
SELECT patron_id, first_name, last_name, street_number, street, unit_number, city, state, zip FROM patrons WHERE patron_id = :patron_id_input
-- Get all drivers info
SELECT drivers.account_id, CONCAT(first_name, ' ', last_name) AS driver_name, license_plate, license_number FROM accounts
INNER JOIN drivers ON drivers.account_id = accounts.account_id
ORDER BY drivers.account_id;
-- Search drivers entity by license number
SELECT driver_id, first_name, last_name, license_plate, license_number FROM drivers WHERE license_number = :license_number_input;
-- Get all chefs info
SELECT chefs.account_id, CONCAT(first_name, ' ', last_name) AS chef_name, cert_number, specialty, type FROM accounts
INNER JOIN chefs ON chefs.account_id = accounts.account_id
ORDER BY chefs.account_id;
-- Search chefs entity by certificate number
SELECT chef_id, first_name, last_name, cert_number, specialty FROM chefs
WHERE cert_number = :cert_number_input;
-- Get all orders with patron's name, address, delivery driver's license plate, order time, total price, and order status
SELECT order_id, CONCAT(first_name, ' ', last_name) AS ordered_by, license_plate AS delivery_by, CONCAT(IFNULL(street_number, ', '), ' ', street, ' ', IFNULL(unit_number, ''), ', ', city, ', ', state, ' ', zip_code) AS patron_address, order_time, total_price, order_status 
FROM orders
INNER JOIN accounts ON orders.ordered_by = accounts.account_id
INNER JOIN patrons ON orders.ordered_by = patrons.account_id
INNER JOIN drivers ON orders.delivery_by = drivers.account_id
ORDER BY order_time DESC;"
-- Search order entity by patron or driver of the order
SELECT order_id, ordered_by, delivery_by, order_time, total_price, order_status FROM orders WHERE ordered_by = :ordered_by_input OR delivery_by = :delivery_by_input OR order_time = :order_time_input;
-- Get all foods information
SELECT * FROM foods;
-- Search foods entity by food name
SELECT food_id, order_id, made_by, food_name, description, is_vegan, is_vegetarian, price FROM foods WHERE food_name = :food_name_input;
-- Get all ingredients information.
SELECT * FROM ingredients;
-- Search ingredients entity by ingredient name
SELECT ingredient_id, ingredient_name, expiry_date, in_stock FROM ingredients WHERE ingredient_name = :ingredient_name_input;
-- Get names of food and its ingredients from the foods_has_ingredients entity.
SELECT f_has_i_id, foods.food_name, ingredients.ingredient_name FROM foods_has_ingredients
INNER JOIN foods ON foods_has_ingredients.food_id = foods.food_id
INNER JOIN ingredients ON foods_has_ingredients.ingredient_id = ingredients.ingredient_id;
-- Search foods_has_ingredients entity based on the name of the food or ingredient.
SELECT f_has_i_id, foods.food_name, ingredients.ingredient_name FROM foods_has_ingredients
INNER JOIN foods ON foods_has_ingredients.food_id = foods.food_id
INNER JOIN ingredients ON foods_has_ingredients.ingredient_id = ingredients.ingredient_id
WHERE foods.food_id = :food_id_input OR ingredients.ingredient_id = :ingredient_id_input;

------------
/* UPDATE */
------------
-- Update account information
UPDATE accounts SET first_name = :first_name_input, last_name = :last_name_input, email = :email_input, password = :password_input, phone_number = :phone_number_input, type = :type_from_dropdown_input WHERE account_id = :account_id_input;
-- Update patron account information
UPDATE patrons SET street_number = :street_number_input, street = :street_input, unit_number = :unit_number_input, city = :city_input, state = :state_input, zip_code = :zip_code_input WHERE account_id = :account_id_input;
-- Update driver account information
UPDATE drivers SET license_plate = :license_place_input, license_number = :license_number_input WHERE account_id = :account_id_input;
-- Update chefs account information
UPDATE chefs SET cert_number = :cert_number_input, specialty = :specialty_input WHERE account_id = :account_id_input;
-- Orders entity will not allow update or delete since it is a transaction table...?
UPDATE orders SET ordered_by = :ordered_by_input, delivery_by = :delivery_by_input, order_time = :order_time_input, total_price = :total_price_input, order_status = :order_status_input WHERE order_id = :order_id_input;
-- Update food information
UPDATE foods SET order_id = :order_id_input, made_by = :made_by_input, food_name = :food_name_input, description = :description_input, is_vegan = :is_vegan_input, is_vegetarian = :is_vegetarian_input, price = :price_input WHERE food_id = :food_id_input;
-- Update ingredient information
UPDATE ingredients SET ingredient_name = :ingredient_name_input, expiry_date = :expiry_date_input, in_stock = :in_stock_input WHERE ingredient_id = :ingredient_name_input;
-- Update foods_has_ingredients
UPDATE foods_has_ingredients SET food_id = :food_id, ingredient_id = :ingredient_id WHERE f_has_i_id = :f_has_i_id_input;

------------
/* DELETE */
------------
-- Delete an account
DELETE FROM accounts WHERE account_id = :account_id_input
-- Orders entity will not allow update or delete since it is a transaction table.
-- Delete food
DELETE FROM foods WHERE food_id = :food_id_input
-- Delete ingredient
DELETE FROM ingredients WHERE ingredient_id = :ingredient_id_input
-- Delete an entry from the foods_has_ingredients table
DELETE FROM foods_has_ingredients WHERE f_has_i_id = :f_has_i_id_input
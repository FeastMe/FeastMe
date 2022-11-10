-- CS340 Fall 2022
-- Group 17 (FeastMe)
-- Bianca Davies
-- Elliott Larsen

/* Create Tables */
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    account_id INT(11) NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    type VARCHAR(1) NOT NULL,
    PRIMARY KEY(account_id)
);

DROP TABLE IF EXISTS patrons;
CREATE TABLE patrons (
    patron_id INT(11) NOT NULL AUTO_INCREMENT,
    account_id INT(11) NOT NULL,
    street_number VARCHAR(45),
    street VARCHAR(255) NOT NULL,
    unit_number VARCHAR(45),
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    zip_code VARCHAR(5) NOT NULL,
    PRIMARY KEY(patron_id),
    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS drivers;
CREATE TABLE drivers (
    driver_id INT(11) NOT NULL AUTO_INCREMENT,
    account_id INT(11) NOT NULL,
    license_plate VARCHAR(45) UNIQUE NOT NULL,
    license_number VARCHAR(45) UNIQUE NOT NULL,
    PRIMARY KEY(driver_id),
    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS chefs;
CREATE TABLE chefs (
    chef_id INT(11) NOT NULL AUTO_INCREMENT,
    account_id INT(11) NOT NULL,
    cert_number VARCHAR(45) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    PRIMARY KEY(chef_id),
    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id INT(11) NOT NULL AUTO_INCREMENT,
    ordered_by INT(11) NOT NULL,
    delivery_by INT(11) NOT NULL,
    order_time DATETIME NOT NULL,
    total_price DECIMAL(65, 2) NOT NULL,
    order_status VARCHAR(255) NOT NULL,
    PRIMARY KEY(order_id),
    FOREIGN KEY(ordered_by) REFERENCES patrons(account_id),
    FOREIGN KEY(delivery_by) REFERENCES drivers(account_id)
);

DROP TABLE IF EXISTS foods;
CREATE TABLE foods (
    food_id INT(11) NOT NULL AUTO_INCREMENT,
    order_id INT(11),
    made_by INT(11),
    food_name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255) NOT NULL,
    is_vegan TINYINT(1) NOT NULL,
    is_vegetarian TINYINT(1) NOT NULL,
    price DECIMAL(65, 2) NOT NULL,
    PRIMARY KEY(food_id),
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(made_by) REFERENCES chefs(account_id)
);

DROP TABLE IF EXISTS ingredients;
CREATE TABLE ingredients (
    ingredient_id INT(11) NOT NULL AUTO_INCREMENT,
    ingredient_name VARCHAR(255) UNIQUE NOT NULL,
    expiry_date DATE NOT NULL,
    in_stock TINYINT(1) NOT NULL,
    PRIMARY KEY(ingredient_id)
);

DROP TABLE IF EXISTS foods_has_ingredients;
CREATE TABLE foods_has_ingredients (
    f_has_i_id INT(11) NOT NULL AUTO_INCREMENT,
    food_id INT(11) NOT NULL,
    ingredient_id INT(11) NOT NULL,
    PRIMARY KEY(f_has_i_id),
    FOREIGN KEY(food_id) REFERENCES foods(food_id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
);

/* Populate Tables */

INSERT INTO accounts(first_name, last_name, email, password, phone_number, type) VALUES
('Karl', 'Johnson', 'kmj8345@gmail.com', 'password125', '419-856-1111', 'C'),
('Sarah', 'Taylor', 'sarahtaylor@live.com',	'qw3rtY71',	'440-778-3265',	'D'),
('Miguel', 'Rivera', 'miguel_cooks46@gmail.com', 'te@#$1209', '440-778-0159', 'C'),
('Toph', 'Li', 'tophrli@gmail.com', 'r&un8Awa0y', '419-255-3107', 'P'),
('Dean', 'Koo', 'koo_dean3@live.com', '5$#79!hi', '440-656-2235', 'P'),
('Mya', 'Parker', 'mparker@gmail.com', 'p0t@t0es', '419-656-4411', 'P'),
('Tom',	'Maan',	'maaningtom@gmail.com',	'OhioLovesMe1',	'419-778-0101',	'D'),
('Ava',	'Park',	'avaleannepark89@gmail.com', 'L@TTe&', '419-997-2000', 'C'),
('Alan', 'Liebowitz', 'liebowitz_49@live.com', 'Forever1', '440-997-6153', 'D'),
('Tako', 'Nielsen', 'takoeatstaco@live.com', 'Tacos800', '440-778-7456', 'P');

INSERT INTO patrons(account_id, street_number, street, unit_number, city, state, zip_code) VALUES
('6', '65010', 'Main Street', NULL, 'Cleveland', 'Ohio', '44109'),
('4', '82829', 'Union Street', '12', 'Akron', 'Ohio', '44301'),
('5', '79404', 'Washington Avenue',	NULL, 'Akron', 'Ohio', '44306'),
('10', '12932', 'Cherry Road', '804', 'Cleveland', 'Ohio', '44105');


INSERT INTO drivers(account_id, license_plate, license_number) VALUES
('2', 'A04CF5', '65885432'),
('7', 'JL779P',	'70015661'),
('9', 'QRS789',	'89993541');

INSERT INTO chefs(account_id, cert_number, specialty) VALUES
('8', 'CN1865', 'sous chef'),
('1', 'NX9644', 'chef'),
('3', 'OL5250', 'pastry chef');

INSERT INTO orders(ordered_by, delivery_by, order_time, total_price, order_status) VALUES
(4, 2, '2022-10-21 06:30:00', '15.95', 'En Route'),
(5, 7, '2022-10-22 11:15:00', '22.00',	'Complete'),
(10, 7,	'2022-10-19 07:28:00', '17.95', 'Complete'),
(6, 2, '2022-10-19 03:00:00', '28.75',	'Ordered'),
(10, 9, '2022-10-20 05:45:00', '19.00', 'En Route');

INSERT INTO foods(order_id, food_name, description, is_vegan, is_vegetarian, price) VALUES
(5, 'Wild Rice Salad', 'Tossed with roasted balsamic brussel sprouts, cranberries, feta, and maple butternut squash.', 0, 1, 11.75),
(1, 'Brown Butter Mushrooms', 'Puffed pastry filled sauteed oyster mushrooms in a brown butter sage sauce, topped with parsley.', 0, 1, 14.00),
(4, 'Miso Orrechiette', 'Orrechiette pasta in a creamy almond miso carrot sauce.', 1, 0, 12.50),
(2, 'Seared Dill Salmon', 'Seared wild atlantic salmon, coated in a dill sauce and tossed with lemon wild rice.', 0, 0, 17.99),
(3, 'Baked Lamb Chops', 'Herbed lamb chops with a spiced bluberry compote and hasselback potatoes',	0, 0, 21.50);

INSERT INTO ingredients(ingredient_name, expiry_date, in_stock) VALUES
('salmon', '2022-10-22', 1),
('brussel sprouts',	'2022-10-25', 0),
('lamb chops', '2022-10-23', 1),
('orecchiette pasta', '2023-12-09', 1),
('carrots',	'2022-11-19', 0),
('wild rice', '2024-04-15',	1),
('oyster mushroom',	'2022-11-02',0),
('blueberry', '2022-10-23',	0),
('olive oil', '2025-06-18',	1),
('garlic', '2023-01-14', 1);

INSERT INTO foods_has_ingredients(food_id, ingredient_id) VALUES
(1, 6),
(1, 2),
(1, 9),
(2, 7),
(3, 4),
(3, 5),
(4, 1),
(4, 9);
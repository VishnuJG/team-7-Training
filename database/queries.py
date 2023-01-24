CREATE_PRODUCT_TABLE = (
  "CREATE TABLE IF NOT EXISTS product_table (uniqueId VARCHAR(10000) PRIMARY KEY NOT NULL, title VARCHAR(10000), description VARCHAR(10000), price VARCHAR(10000), image_url VARCHAR(10000), category_id INTEGER);"
)

CREATE_CATEGORY_TABLE = (
  "CREATE TABLE IF NOT EXISTS category_table(category_id SERIAL PRIMARY KEY NOT NULL, category_name VARCHAR(10000), parent_name VARCHAR(10000), UNIQUE(category_id));"
)
# , FOREIGN KEY(category_id) REFERENCES product_table(category_id) ON DELETE CASCADE

INSERT_PRODUCT = (
  "INSERT INTO product_table (uniqueId, title, description, price, image_url, category_id) VALUES(%s, %s, %s, %s, %s, %s);"
)

SELECT_ALL_PRODUCTS = (
    "Select * from product_table;"
)

GET_PRODUCT = (
    "SELECT * FROM product_table WHERE uniqueID = (%s)"
)

CATEGORY_ID_EXISTS = (
  "SELECT EXISTS (SELECT category_id from category_table WHERE category_name = (%s) AND parent_name = (%s));"
)

GET_CATEGORY_ID = (
  "SELECT category_id from category_table WHERE category_name = %s AND parent_name = %s;"
)

INSERT_CATEGORY_ID = (
  "INSERT INTO category_table(category_name, parent_name) VALUES (%s, %s);"
)

GET_CATEGORY_PRODUCTS = (
  "SELECT uniqueId, title, description, price, image_url from product_table WHERE category_id = (%s);"
)

GET_SUBCATEGORY_NAMES = (
  "SELECT category_name from category_table where parent_name = (%s);"
)
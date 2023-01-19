CREATE_PRODUCT_TABLE = (
  "CREATE TABLE IF NOT EXISTS product_table (uniqueId TEXT PRIMARY KEY NOT NULL, title TEXT, description TEXT, price NUMERIC, image_url TEXT, categoryId INTEGER);"
)

CREATE_CATEGORY_TABLE = (
  "CREATE TABLE IF NOT EXISTS category_table(categoryId numeric PRIMARY KEY, category_name TEXT, parent_id INTEGER, FOREIGN KEY(categoryId) REFERENCES product_table(categoryId) ON DELETE CASCADE);"
)

SELECT_ALL_PRODUCTS = (
    "Select * from product_table;"
)

GET_PRODUCT = (
    "SELECT * FROM product_table WHERE uniqueID = (%s)"
)
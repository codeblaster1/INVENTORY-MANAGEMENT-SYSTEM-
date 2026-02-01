CREATE DATABASE inventory;

USE inventory;


-- Create the Categories table

CREATE TABLE categories (
 categoryid INT PRIMARY KEY auto_increment,
 categoryname VARCHAR(255) NOT NULL
 );


-- Create the Suppliers table

CREATE TABLE suppliers (
 supplierid INT PRIMARY KEY auto_increment,
 suppliername VARCHAR(255) NOT NULL,
 contactinfo VARCHAR(255),
 address VARCHAR(255),
 email VARCHAR(255),
 phone VARCHAR(20)
 );
 
 
 
-- Create the Products table

CREATE TABLE products (
 productid INT PRIMARY KEY auto_increment,
 productname VARCHAR(255) NOT NULL,
 description TEXT,
 categoryid INT,
 price DECIMAL(10, 2) NOT NULL,
 stockquantity INT NOT NULL,
 reorderlevel INT,
 supplierid INT,
 dateadded DATE,
 FOREIGN KEY (categoryid) REFERENCES categories(categoryid),
 FOREIGN KEY (supplierid) REFERENCES suppliers(supplierid)
 );
 
 
-- Create the Sales table

CREATE TABLE sales (
 saleid INT PRIMARY KEY auto_increment,
 productid INT,
 quantitysold INT NOT NULL,
 saledate DATE NOT NULL,
 totalamount DECIMAL(10, 2) NOT NULL,
 FOREIGN KEY (productid) REFERENCES products(productid)
 );
 
 
-- Insert sample data into the Categories table
INSERT INTO categories(categoryname)
VALUES ('Electronics'),
('Clothing'),
('Furniture'),
('Toys');



-- Insert sample data into the Suppliers table

INSERT INTO suppliers (suppliername,contactinfo,address,email, phone)
VALUES ('ABC Electronics','123 Main St','City, State','abc@example.com','123-456-7890'),
 ('Fashion House','456 Elm St','City, State','fashion@example.com','987-654-3210'),
 ('Furniture World','789 Oak St','City, State','furniture@example.com','555-123-4567'),
 ('Toy Universe','101 Maple St','City, State','toys@example.com','111-222-3333');
 
 
-- Insert sample data into the Products table

INSERT INTO products (productname,description,categoryid,price,stockquantity,reorderlevel,supplierid,dateadded)
VALUES ('Smartphone X','High-end smartphone',1,699.99,100,10,1,'2023-01-15'),
 ('LED TV 55"','4K UHD Smart TV',1,799.99,50,5,1,'2023-02-10'),
 ('Men''s Jacket','Winter jacket',2,79.99,150,20,2,'2023-03-20'),
 ('Coffee Table','Wooden coffee table',3,149.99,30,5,3,'2023-04-05'),
 ('LEGO Set','Building blocks',4,49.99,200,30,4,'2023-05-15');
 
 
 SHOW tables;
 
 SELECT * FROM products;
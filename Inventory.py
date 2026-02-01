from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox

# Establish a MySQL connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLmydataforjob@2026",
    database="inventory",
    port=3306,
    auth_plugin="mysql_native_password"
)
# Create a cursor object
cursor = db.cursor()

# Function to open the main menu window
def main_menu():
    menu_window = Tk()
    menu_window.title("Inventory Management - Main Menu")

    # Function to open the "Update Products" page
    def open_update_products_page():
        menu_window.destroy()  # Close the main menu window
        update_products_page()

    # Function to open the "New Order" page
    def open_new_order_page():
        menu_window.destroy()  # Close the main menu window
        new_order_page()

    # Create buttons for choosing between new order and update products
    new_order_button = Button(menu_window, text="New Order", command=open_new_order_page)
    update_products_button = Button(menu_window, text="Update Products", command=open_update_products_page)
    new_order_button.pack(pady=20)
    update_products_button.pack()
    menu_window.mainloop()

# Function to open the "New Order" page
def new_order_page():
    order_window = Tk()
    order_window.title("New Order")

    def add_to_cart():
        product_name = product_name_entry.get()
        quantity = quantity_entry.get()
        if not product_name or not quantity:
            messagebox.showerror("Error", "Please enter product name and quantity.")
            return

        # Fetch product information from the database
        query = "SELECT ProductID, Price, StockQuantity FROM Products WHERE ProductName = %s"
        cursor.execute(query, (product_name,))
        product = cursor.fetchone()
        if product:
            product_id, price, stock_quantity = product
            quantity = int(quantity)
            if stock_quantity < quantity:
                messagebox.showerror("Error", "Not enough stock available.")
                return
            total = quantity * price
            order_tree.insert("", "end", values=(product_id, product_name, quantity, price, total))
        else:
            messagebox.showerror("Error", "Product not found!")
        product_name_entry.delete(0, END)
        quantity_entry.delete(0, END)

    def checkout():
        for item in order_tree.get_children():
            product_id = order_tree.item(item, "values")[0]
            quantity = int(order_tree.item(item, "values")[2])
            # Update stock quantity in the database
            update_stock_query = "UPDATE Products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s"
            cursor.execute(update_stock_query, (quantity, product_id))
            db.commit()
        messagebox.showinfo("Success", "Checkout completed.")

    # Create and configure UI elements
    product_name_label = Label(order_window, text="Product Name")
    product_name_label.grid(row=0, column=0)
    product_name_entry = Entry(order_window)
    product_name_entry.grid(row=0, column=1)
    quantity_label = Label(order_window, text="Quantity")
    quantity_label.grid(row=1, column=0)
    quantity_entry = Entry(order_window)
    quantity_entry.grid(row=1, column=1)
    add_to_cart_button = Button(order_window, text="Add to Cart", command=add_to_cart)
    add_to_cart_button.grid(row=2, column=0, columnspan=2)

    # Create a Treeview widget to display the order in a table-like format
    order_tree = ttk.Treeview(order_window, columns=("ProductID", "ProductName", "Quantity", "Price", "Total"))
    order_tree.heading("ProductID", text="Product ID")
    order_tree.heading("ProductName", text="Product Name")
    order_tree.heading("Quantity", text="Quantity")
    order_tree.heading("Price", text="Price")
    order_tree.heading("Total", text="Total")
    order_tree.column("#1", width=100, anchor="center")
    order_tree.column("#2", width=250, anchor="center")
    order_tree.column("#3", width=100, anchor="center")
    order_tree.column("#4", width=100, anchor="center")
    order_tree.column("#5", width=100, anchor="center")
    order_tree["show"] = "headings"
    order_tree.grid(row=3, column=0, columnspan=2)
    checkout_button = Button(order_window, text="Checkout", command=checkout)
    checkout_button.grid(row=4, column=0, columnspan=2)
    order_window.mainloop()

# Function to update product information in the database
def update_products_page():
    update_window = Tk()
    update_window.title("Update Products")

    def add_product():
        product_name = product_name_entry.get()
        description = description_entry.get()
        category_id = category_id_entry.get()
        price = price_entry.get()
        stock_quantity = stock_quantity_entry.get()
        query = "INSERT INTO Products (ProductName, Description, CategoryID, Price, StockQuantity) VALUES (%s, %s, %s, %s, %s)"
        values = (product_name, description, category_id, price, stock_quantity)
        cursor.execute(query, values)
        db.commit()
        product_name_entry.delete(0, END)
        description_entry.delete(0, END)
        category_id_entry.delete(0, END)
        price_entry.delete(0, END)
        stock_quantity_entry.delete(0, END)
        view_products()

    def delete_product():
        product_id = product_id_entry.get()
        query = "DELETE FROM Products WHERE ProductID = %s"
        value = (product_id,)
        cursor.execute(query, value)
        db.commit()
        product_id_entry.delete(0, END)
        view_products()

    def update_product():
        product_id = product_id_entry.get()
        new_stock_quantity = new_stock_quantity_entry.get()
        query = "UPDATE Products SET StockQuantity = %s WHERE ProductID = %s"
        values = (new_stock_quantity, product_id)
        cursor.execute(query, values)
        db.commit()
        product_id_entry.delete(0, END)
        new_stock_quantity_entry.delete(0, END)
        view_products()

    # Create and configure UI elements for the "Update Products" page
    product_name_label = Label(update_window, text="Product Name")
    product_name_label.grid(row=0, column=0)
    product_name_entry = Entry(update_window)
    product_name_entry.grid(row=0, column=1)
    description_label = Label(update_window, text="Description")
    description_label.grid(row=1, column=0)
    description_entry = Entry(update_window)
    description_entry.grid(row=1, column=1)
    category_id_label = Label(update_window, text="Category ID")
    category_id_label.grid(row=2, column=0)
    category_id_entry = Entry(update_window)
    category_id_entry.grid(row=2, column=1)
    price_label = Label(update_window, text="Price")
    price_label.grid(row=3, column=0)
    price_entry = Entry(update_window)
    price_entry.grid(row=3, column=1)
    stock_quantity_label = Label(update_window, text="Stock Quantity")
    stock_quantity_label.grid(row=4, column=0)
    stock_quantity_entry = Entry(update_window)
    stock_quantity_entry.grid(row=4, column=1)
    add_button = Button(update_window, text="Add Product", command=add_product)
    add_button.grid(row=5, column=0, columnspan=2)
    update_button = Button(update_window, text="Update", command=update_product)
    update_button.grid(row=5, column=3, columnspan=2)

    # Create a Treeview widget to display products in a table-like format
    products_tree = ttk.Treeview(update_window, columns=("ProductID", "ProductName", "Description", "CategoryID", "Price", "StockQuantity"))
    products_tree.heading("ProductID", text="Product ID")
    products_tree.heading("ProductName", text="Product Name")
    products_tree.heading("Description", text="Description")
    products_tree.heading("CategoryID", text="Category ID")
    products_tree.heading("Price", text="Price")
    products_tree.heading("StockQuantity", text="Stock Qty")
    products_tree.column("#1", width=120, anchor="center")
    products_tree.column("#2", width=210, anchor="center")
    products_tree.column("#3", width=270, anchor="center")
    products_tree.column("#4", width=175, anchor="center")
    products_tree.column("#5", width=120, anchor="center")
    products_tree.column("#6", width=150, anchor="center")
    products_tree["show"] = "headings"
    products_tree.grid(row=0, column=2, rowspan=6, columnspan=4)

    # Additional UI elements and buttons for delete and update operations
    product_id_label = Label(update_window, text="Product ID (for delete/update)")
    product_id_label.grid(row=7, column=0)
    product_id_entry = Entry(update_window)
    product_id_entry.grid(row=7, column=1)
    delete_button = Button(update_window, text="Delete Product", command=delete_product)
    delete_button.grid(row=8, column=0, columnspan=2)
    new_stock_quantity_label = Label(update_window, text="New Stock Quantity (for update)")
    new_stock_quantity_label.grid(row=9, column=0)
    new_stock_quantity_entry = Entry(update_window)
    new_stock_quantity_entry.grid(row=9, column=1)
    update_button = Button(update_window, text="Update Stock Quantity", command=update_product)
    update_button.grid(row=10, column=0, columnspan=2)

    # Function to query products from the database and display them in the UI
    def view_products():
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        # Clear the Treeview widget
        for item in products_tree.get_children():
            products_tree.delete(item)
        for product in products:
            products_tree.insert("", "end", values=product)

    # Start the UI main loop
    view_products()  # Load initial product data
    update_window.mainloop()

# Start the application by showing the main menu
main_menu()

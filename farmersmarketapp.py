import sqlite3
import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from tkinter import font

# Set up SQLite database connection
conn = sqlite3.connect('farmers_market.db')
cursor = conn.cursor()

# Database setup for Farmer and Product tables
# Set up SQLite database connection
conn = sqlite3.connect('farmers_market.db')
cursor = conn.cursor()

# Database setup for Farmer and Product tables
def setup_database():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Farmer (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        location TEXT,
                        language TEXT,
                        mobile_number TEXT)''')  # Only 'mobile_number' remains
    
cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     farmer_id TEXT,
                     name TEXT,
                     Price REAL,
                     quantity REAL,
                     demand_score REAL,
                     FOREIGN KEY (farmer_id) REFERENCES Farmer(id))''')
conn.commit()


conn.commit()

# Call setup_database to ensure tables are created
setup_database()


# Machine Learning Models
from model_creation import demand_model, price_model

# Database functions
def register_farmer(farmer_id, name, location, language, mobile_number):
    cursor.execute("SELECT id FROM Farmer WHERE id=?", (farmer_id,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Farmer ID already exists. Please choose a unique ID.")
        return False
    cursor.execute("INSERT INTO Farmer (id, name, location, language, mobile_number) VALUES (?, ?, ?, ?, ?)", 
                   (farmer_id, name, location, language, mobile_number))
    conn.commit()
    return True

def add_mobile_number_column():
    try:
        cursor.execute("ALTER TABLE Farmer ADD COLUMN mobile_number TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # This error occurs if the column already exists
        pass
setup_database()
add_mobile_number_column()


def list_product(farmer_id, name, price, quantity):
    demand_features = np.array([[price, quantity]])
    demand_score = demand_model.predict(demand_features)[0]
    cursor.execute("INSERT INTO Product (farmer_id, name, Price, quantity, demand_score) VALUES (?, ?, ?, ?, ?) ",
                   (farmer_id, name, price, quantity, demand_score))
    conn.commit()
    refresh_consumer_section()  # Uncomment this line if you want to refresh consumer section on new product addition
    return demand_score

def update_product_price(farmer_id, product_name, new_price):
    cursor.execute("UPDATE Product SET price=? WHERE farmer_id=? AND name=?", (new_price, farmer_id, product_name))
    conn.commit()
    refresh_consumer_section()

def recommend_price(demand_score):
    recommended_price = price_model.predict(np.array([[demand_score]]))[0]
    return recommended_price

def get_all_products():
    cursor.execute("SELECT Product.*, Farmer.location FROM Product JOIN Farmer ON Product.farmer_id = Farmer.id")
    return cursor.fetchall()

# GUI Setup
root = tk.Tk()
root.title("Farmers Market Management")
root.geometry("400x700")
root.config(bg="white")

# Fonts
header_font = font.Font(family="Helvetica", size=16, weight="bold", slant="italic")
section_font = font.Font(family="Helvetica", size=12, weight="bold")

# Create frames for different sections
frames = {}

def create_frame(name):
    frame = tk.Frame(root, bg="white")
    frames[name] = frame
    return frame

# Function to show a specific frame
def show_frame(frame_name):
    for frame in frames.values():
        frame.pack_forget()
    frames[frame_name].pack(expand=True)

# Home Frame with Navigation Buttons
home_frame = create_frame("Home")
home_label = tk.Label(home_frame, text="Farmers Market", font=header_font, bg="white", fg="black")
home_label.pack(pady=(10, 5))

# "Selling" heading with space
selling_label = tk.Label(home_frame, text="Selling", font=("Helvetica", 14, "bold"), bg="white", fg="black")
selling_label.pack(pady=(20, 5))

# Navigation Buttons
nav_frame = tk.Frame(home_frame, bg="white")
nav_frame.pack(pady=10)

def create_nav_button(text, command):
    button = tk.Button(nav_frame, text=text, command=command, bg="yellow", fg="black", borderwidth=0, relief="flat")
    button.pack(pady=10, fill=tk.X)
    button.config(font=("Helvetica", 12))

nav_buttons = [
    ("Register Farmer", lambda: show_frame("Register Farmer")),
    ("List Product", lambda: show_frame("List Product")),
    ("Recommend Price", lambda: show_frame("Recommend Price")),
    ("Update Product Price", lambda: show_frame("Update Price")),
]

for btn_text, btn_command in nav_buttons:
    create_nav_button(btn_text, btn_command)

# "Buying" heading
buying_label = tk.Label(nav_frame, text="Buying", font=("Helvetica", 14, "bold"), bg="white", fg="black")
buying_label.pack(pady=(20, 5))

# Add Consumer Section Button
create_nav_button("Consumer Section", lambda: show_frame("Consumer Section"))

# Register Farmer GUI
def register_farmer_gui():
    frame = create_frame("Register Farmer")
    
    def on_submit():
        farmer_id = farmer_id_entry.get()
        name = name_entry.get()
        location = location_entry.get()
        language = language_entry.get()
        mobile_number = mobile_number_entry.get()  # Only mobile number is captured now
        
        if register_farmer(farmer_id, name, location, language, mobile_number):
            messagebox.showinfo("Success", "Farmer registered successfully!")
            show_frame("Home")

    tk.Label(frame, text="Register Farmer", font=section_font, bg="white", fg="black").pack(pady=10)
    tk.Label(frame, text="Farmer ID").pack()
    farmer_id_entry = tk.Entry(frame)
    farmer_id_entry.pack()

    tk.Label(frame, text="Name").pack()
    name_entry = tk.Entry(frame)
    name_entry.pack()

    tk.Label(frame, text="Location").pack()
    location_entry = tk.Entry(frame)
    location_entry.pack()

    tk.Label(frame, text="Language").pack()
    language_entry = tk.Entry(frame)
    language_entry.pack()
    
    tk.Label(frame, text="Mobile Number").pack()  # Only Mobile Number remains
    mobile_number_entry = tk.Entry(frame)
    mobile_number_entry.pack()

    tk.Button(frame, text="Submit", command=on_submit, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)
    frame.pack(expand=True)

register_farmer_gui()

# List Product GUI
def list_product_gui():
    frame = create_frame("List Product")
    def on_submit():
        farmer_id = farmer_id_entry.get()
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = float(quantity_entry.get())
        demand_score = list_product(farmer_id, name, price, quantity)
        messagebox.showinfo("Product Listed", f"Product listed with demand score: {demand_score:.2f}")
        show_frame("Home")

    tk.Label(frame, text="List Product", font=section_font, bg="white", fg="black").pack(pady=10)
    tk.Label(frame, text="Farmer ID").pack()
    farmer_id_entry = tk.Entry(frame)
    farmer_id_entry.pack()

    tk.Label(frame, text="Product Name").pack()  # Changed label to "Product Name"
    name_entry = tk.Entry(frame)
    name_entry.pack()

    tk.Label(frame, text="Price").pack()
    price_entry = tk.Entry(frame)
    price_entry.pack()

    tk.Label(frame, text="Quantity").pack()
    quantity_entry = tk.Entry(frame)
    quantity_entry.pack()

    tk.Button(frame, text="Submit", command=on_submit, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)  # Added Back button
    frame.pack(expand=True)

list_product_gui()

# Update Product Price GUI
def update_price_gui():
    frame = create_frame("Update Price")
    def on_submit():
        farmer_id = farmer_id_entry.get()
        product_name = product_name_entry.get()
        new_price = float(new_price_entry.get())
        update_product_price(farmer_id, product_name, new_price)
        messagebox.showinfo("Success", "Product price updated successfully!")
        show_frame("Home")

    tk.Label(frame, text="Update Product Price", font=section_font, bg="white", fg="black").pack(pady=10)
    tk.Label(frame, text="Farmer ID").pack()
    farmer_id_entry = tk.Entry(frame)
    farmer_id_entry.pack()

    tk.Label(frame, text="Product Name").pack()
    product_name_entry = tk.Entry(frame)
    product_name_entry.pack()

    tk.Label(frame, text="New Price").pack()
    new_price_entry = tk.Entry(frame)
    new_price_entry.pack()

    tk.Button(frame, text="Submit", command=on_submit, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)
    frame.pack(expand=True)

update_price_gui()

# Recommend Price GUI
def recommend_price_gui():
    frame = create_frame("Recommend Price")

    def on_submit():
        farmer_id = farmer_id_entry.get()
        product_name = product_name_entry.get()

        # Fetch the product details to get the demand score
        cursor.execute("SELECT price, quantity, demand_score FROM Product WHERE farmer_id=? AND name=?", (farmer_id, product_name))
        product = cursor.fetchone()
        
        if product:
            price, quantity, demand_score = product
            recommended_price = recommend_price(demand_score)
            messagebox.showinfo("Recommendation", f"Demand Score: {demand_score:.2f}\nRecommended Price: ${recommended_price:.2f}")
        else:
            messagebox.showerror("Error", "Product not found. Please check the Farmer ID and Product Name.")

    tk.Label(frame, text="Recommend Price", font=section_font, bg="white", fg="black").pack(pady=10)

    tk.Label(frame, text="Farmer ID").pack()
    farmer_id_entry = tk.Entry(frame)
    farmer_id_entry.pack()

    tk.Label(frame, text="Product Name").pack()
    product_name_entry = tk.Entry(frame)
    product_name_entry.pack()

    tk.Button(frame, text="Submit", command=on_submit, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)

    frame.pack(expand=True)

recommend_price_gui()


# Consumer Section GUI
def consumer_section_gui():
    frame = create_frame("Consumer Section")  # Create and define the frame for the consumer section

    def display_products():
        products = get_all_products()
        for widget in product_frame.winfo_children():
            widget.destroy()  # Clear previous products

        for product in products:
            product_name = product[2]
            price = product[3] if product[3] is not None else 0  # Default to 0 if None
            quantity = product[4] if product[4] is not None else 0  # Default to 0 if None
            farmer_id = product[1]  # Get farmer ID for details

            # Display product information
            product_label = tk.Label(product_frame, text=f"Product Name: {product_name}, Price: ${price:.2f}, Quantity: {quantity}", bg="white")
            product_label.pack()

            # Add a purchase button with a lambda to capture farmer_id
            purchase_button = tk.Button(product_frame, text="Purchase", command=lambda fid=farmer_id: show_farmer_details(fid), bg="yellow", fg="black")
            purchase_button.pack(pady=5)

    def show_farmer_details(fid):
        cursor.execute("SELECT name, id, location, language, mobile_number FROM Farmer WHERE id=?", (fid,))
        farmer = cursor.fetchone()
        if farmer:
            farmer_name, farmer_id, location, language, mobile_number = farmer
            # Display all registered farmer details in a message box
            messagebox.showinfo("Farmer Details", f"Farmer Name: {farmer_name}\nFarmer ID: {farmer_id}\nLocation: {location}\nLanguage: {language}\nMobile Number: {mobile_number}")
        else:
            messagebox.showerror("Error", "Farmer details not found.")

    product_frame = tk.Frame(frame, bg="white")
    product_frame.pack(pady=10)

    display_products()  # Display products initially

    tk.Button(frame, text="Refresh", command=display_products, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)

    frame.pack(expand=True)
consumer_section_gui ()





# Start with the Home frame
show_frame("Home")

# Run the application
root.mainloop()

# Clean up database connection when done
conn.close()
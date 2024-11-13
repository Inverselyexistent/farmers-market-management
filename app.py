import sqlite3
import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from tkinter import font
import sqlite3
from sklearn.preprocessing import LabelEncoder
import pandas as pd

df = pd.read_csv(r"D:\direct farm\farmers_market_data.csv")

# Set up SQLite database connection
conn = sqlite3.connect('farmers__market.db')
cursor = conn.cursor()

# Database setup for Farmer and Product tables
def setup_database():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Farmer (
                        id TEXT PRIMARY KEY,py
                        name TEXT NOT NULL,
                        location TEXT,
                        language TEXT,
                        mobile_number TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        farmer_id TEXT,
                        Commodity TEXT,
                        Price REAL,
                        FOREIGN KEY (farmer_id) REFERENCES Farmer(id))''')
    
    conn.commit()

# Call setup_database to ensure tables are created
setup_database()



# Machine Learning Models
from model import demand_model, price_model

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

label_encoder = LabelEncoder()
df['Commodity_encoded'] = label_encoder.fit_transform(df['Commodity'])

def list_product(farmer_id, Commodity , price):
    cursor.execute("INSERT INTO Product (farmer_id, Commodity, Price) VALUES (?, ?, ?) ",
                   (farmer_id, Commodity , price))
    conn.commit()
    refresh_consumer_section()  # Uncomment this line if you want to refresh consumer section on new product addition
    return True

def update_product_price(farmer_id, Commodity , new_price):
    cursor.execute("UPDATE Product SET price=? WHERE farmer_id=? AND name=?", (new_price, farmer_id, Commodity))    
    conn.commit()
    refresh_consumer_section()

def predict_recommended_price(commodity, modal_price):
    commodity_encoded = label_encoder.transform([commodity])[0]
    recommended_price = price_model.predict([[commodity_encoded, modal_price,]])[0]
    return recommended_price
def predict_demand(price, recommended_price):
    demand = demand_model.predict([[price, recommended_price]])[0]
    return demand

def get_all_products():
    cursor.execute("SELECT Product.*, Farmer.location FROM Product JOIN Farmer ON Product.farmer_id = Farmer.id")
    return cursor.fetchall()

def refresh_consumer_section():
    product_frame = tk.Frame(root, bg="white")
    product_frame.pack(pady=10)

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
import tkinter as tk
from tkinter import messagebox

# List Product GUI function
def list_product_gui():
    frame = create_frame("List Product")

    # Create Entry widgets for farmer ID, Commodity, and price
    farmer_id_entry = tk.Entry(frame)
    commodity_entry = tk.Entry(frame)
    price_entry = tk.Entry(frame)

    # Define the submit action
    def on_submit():
        try:
            # Get input values
            farmer_id = farmer_id_entry.get()
            commodity = commodity_entry.get()
            price = float(price_entry.get())

            # Ensure 'cursor' is available and connected to the database
            global cursor
            if cursor is None:
                raise ValueError("Database connection not established.")

            # Fetch the product details to check if it exists
            cursor.execute("SELECT farmer_id, Commodity, Price FROM Product WHERE farmer_id=? AND Commodity=?", (farmer_id, commodity))
            product = cursor.fetchone()

            if product:
                # Update existing product if it already exists
                cursor.execute("UPDATE Product SET Price = ? WHERE farmer_id = ? AND Commodity = ?", (price, farmer_id, commodity))
                messagebox.showinfo("Info", "Product updated successfully.")
            else:
                # Insert new product if it doesn't exist
                cursor.execute("INSERT INTO Product (farmer_id, Commodity, Price) VALUES (?, ?, ?)", (farmer_id, commodity, price))
                messagebox.showinfo("Info", "Product listed successfully.")
            
            # Calculate the demand score (add your calculation logic here if needed)
            # For example, let's assume demand_score is a placeholder for actual calculation
            demand_score = calculate_demand_score(price)  # Define this function based on your model
            print(f"Demand Score: {demand_score}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Add widgets to the frame
    tk.Label(frame, text="List Product", font=section_font, bg="white", fg="black").pack(pady=10)
    tk.Label(frame, text="Farmer ID").pack()
    farmer_id_entry.pack()

    tk.Label(frame, text="Commodity").pack()
    commodity_entry.pack()

    tk.Label(frame, text="Price").pack()
    price_entry.pack()

    tk.Button(frame, text="Submit", command=on_submit, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)
    frame.pack(expand=True)

# Example demand score calculation function (replace with your actual logic)
def calculate_demand_score(price):
    # Placeholder function - replace with your demand prediction logic
    return "High" if price < 1000 else "Low"

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

    tk.Label(frame, text="Commodity").pack()
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
# Recommend Price GUI
def recommend_price_gui():
    frame = create_frame("Recommend Price")

    def on_submit():
        farmer_id = farmer_id_entry.get()
        Commodity = Commodity_entry.get()
        price = float(price_entry.get())
        # Fetch the product details to get the demand score
        cursor.execute("SELECT price, Commodity FROM Product WHERE farmer_id=? AND Commodity=?", (farmer_id, Commodity))
        product = cursor.fetchone()
        
        if product:
            price, Commodity = product[0], product[1]  # product_price = fetched price, product_commodity = fetched commodity
            recommended_price = predict_recommended_price(Commodity, price)
            demand_prediction = predict_demand(price, recommended_price)
            messagebox.showinfo("Recommendation",
                        f"Recommended Price: ${recommended_price:.2f}\n"
                        f"Demand Prediction: {demand_prediction}")
        else:
            messagebox.showerror("Error", "Product not found. Please check the Farmer ID and Product Name.")
            

    tk.Label(frame, text="Recommend Price", font=section_font, bg="white", fg="black").pack(pady=10)
    tk.Label(frame, text="Farmer ID").pack()
    farmer_id_entry = tk.Entry(frame)
    farmer_id_entry.pack()

    tk.Label(frame, text="Commodity").pack()
    Commodity_entry= tk.Entry(frame)
    Commodity_entry.pack()

    tk.Label(frame, text="Price").pack()
    price_entry = tk.Entry(frame)  # Define the Price entry
    price_entry.pack()

    tk.Button(frame, text="Submit", command=on_submit, bg="yellow", fg="black").pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)
    
    frame.pack(expand=True)

recommend_price_gui()

def consumer_section_gui():
    frame = create_frame("Consumer Section")  # Create and define the frame for the consumer section

    global product_frame  # Declare product_frame as a global variable to avoid UnboundLocalError
    product_frame = tk.Frame(frame, bg="white")
    product_frame.pack(pady=10)

    def display_products():
        # Get all products from the database
        products = get_all_products()

        # Clear previous products display
        for widget in product_frame.winfo_children():
            widget.destroy()

        # Loop through products and display them
        for product in products:
            Commodity = product[2]
            price = product[3] if product[3] is not None else 0  # Default to 0 if None
            farmer_id = product[1]  # Get farmer ID for details

            # Create a label for each product and add it to the display
            product_label = tk.Label(product_frame, text=f"Commodity: {Commodity}, Price: ${price:.2f}", bg="white")
            product_label.pack()

            # Add a purchase button with a lambda to capture farmer_id
            purchase_button = tk.Button(product_frame, text="Purchase", command=lambda fid=farmer_id: show_farmer_details(fid), bg="yellow", fg="black")
            purchase_button.pack(pady=5)

    def show_farmer_details(fid):
        cursor.execute("SELECT name, id, location, language, mobile_number FROM Farmer WHERE id=?", (fid,))
        farmer = cursor.fetchone()
        if farmer:
            farmer_name, farmer_id, location, language, mobile_number = farmer
            # Display farmer details in a message box
            messagebox.showinfo("Farmer Details", f"Farmer Name: {farmer_name}\nFarmer ID: {farmer_id}\nLocation: {location}\nLanguage: {language}\nMobile Number: {mobile_number}")
        else:
            messagebox.showerror("Error", "Farmer details not found.")

    display_products()  # Display products initially

    # Add refresh button to update the list of products
    tk.Button(frame, text="Refresh", command=display_products, bg="yellow", fg="black").pack(pady=5)

    # Add Back button to go back to the Home screen
    tk.Button(frame, text="Back", command=lambda: show_frame("Home"), bg="yellow", fg="black").pack(pady=5)

    frame.pack(expand=True)
consumer_section_gui()





# Start with the Home frame
show_frame("Home")

# Run the application
root.mainloop()

# Clean up database connection when done
conn.close()
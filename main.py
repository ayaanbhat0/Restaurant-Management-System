import os
import hashlib
import uuid

# File paths
ORDERS_FILE = "orders.txt"
FEEDBACK_FILE = "feedback.txt"
CUSTOMER_FILE = "customers.txt"
STAFF_FILE = "staff.txt"
MENU_FILE = "menu.txt"
INGREDIENTS_FILE = "ingredients.txt"

# Utility Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def write_to_file(file_path, data, mode="a"):
    with open(file_path, mode) as file:
        file.write(data)

def read_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.readlines()
    return []

# Customer Functions
def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)
    
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, "r") as file:
            for line in file:
                stored_username, _ = line.strip().split(',')
                if stored_username == username:
                    print("Username already exists. Try a different one.")
                    return False
    
    write_to_file(CUSTOMER_FILE, f"{username},{hashed_password}\n")
    print("Signup successful!")
    return True

def login(file_path):
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == hashed_password:
                    print("Login successful!")
                    return username
    print("Invalid username or password.")
    return None

def customer_menu(customer_id):
    while True:
        print("\nCustomer Menu:")
        print("1. View Orders")
        print("2. Add Order")
        print("3. Edit Order")
        print("4. Delete Order")
        print("5. Send Feedback")
        print("6. Logout")
        choice = input("Select an option: ")
        
        if choice == "1":
            view_orders(customer_id)
        elif choice == "2":
            item_name = input("Enter item name: ")
            quantity = input("Enter quantity: ")
            order_details = f"{item_name} x{quantity}"
            add_order(customer_id, order_details)
        elif choice == "3":
            order_id = input("Enter Order ID to edit: ")
            new_item_name = input("Enter new item name: ")
            new_quantity = input("Enter new quantity: ")
            new_order_details = f"{new_item_name} x{new_quantity}"
            edit_order(customer_id, order_id, new_order_details)
        elif choice == "4":
            order_id = input("Enter Order ID to delete: ")
            delete_order(customer_id, order_id)
        elif choice == "5":
            feedback = input("Enter your feedback: ")
            send_feedback(customer_id, feedback)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def view_orders(customer_id):
    orders = read_from_file(ORDERS_FILE)
    for order in orders:
        if order.startswith(f"{customer_id}"):
            print(order.strip())

def add_order(customer_id, order_details):
    order_id = str(uuid.uuid4())
    write_to_file(ORDERS_FILE, f"{customer_id},{order_id},{order_details},In Progress\n")
    print(f"Order added with ID: {order_id}")

def edit_order(customer_id, order_id, new_order_details):
    orders = read_from_file(ORDERS_FILE)
    with open(ORDERS_FILE, "w") as file:
        for order in orders:
            parts = order.strip().split(',')
            if parts[0] == customer_id and parts[1] == order_id:
                file.write(f"{customer_id},{order_id},{new_order_details},{parts[3]}\n")
                print("Order updated successfully.")
            else:
                file.write(order)

def delete_order(customer_id, order_id):
    orders = read_from_file(ORDERS_FILE)
    with open(ORDERS_FILE, "w") as file:
        for order in orders:
            parts = order.strip().split(',')
            if not (parts[0] == customer_id and parts[1] == order_id):
                file.write(order)
    print("Order deleted successfully.")

def send_feedback(customer_id, feedback):
    write_to_file(FEEDBACK_FILE, f"{customer_id},{feedback}\n")
    print("Feedback sent successfully.")

# Chef Functions
def chef_menu():
    while True:
        print("\nChef Menu:")
        print("1. View Orders")
        print("2. Update Order Status")
        print("3. Request Ingredients")
        print("4. Update Profile")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_orders_for_chef()
        elif choice == "2":
            update_order_status()
        elif choice == "3":
            request_ingredients()
        elif choice == "4":
            update_chef_profile()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def view_orders_for_chef():
    orders = read_from_file(ORDERS_FILE)
    for order in orders:
        print(order.strip())

def update_order_status():
    orders = read_from_file(ORDERS_FILE)
    order_id = input("Enter Order ID to update: ")
    new_status = input("Enter new status (e.g., In Progress, Completed): ")

    with open(ORDERS_FILE, "w") as file:
        for order in orders:
            parts = order.strip().split(',')
            if parts[1] == order_id:
                file.write(f"{parts[0]},{order_id},{parts[2]},{new_status}\n")
                print("Order status updated.")
            else:
                file.write(order)

def request_ingredients():
    while True:
        print("\nIngredient Request Menu:")
        print("1. Add Ingredient")
        print("2. Edit Ingredient")
        print("3. Delete Ingredient")
        print("4. Go Back")
        choice = input("Enter your choice: ")
        
        ingredients = read_from_file(INGREDIENTS_FILE)
        
        if choice == '1':
            new_ingredient = input("Enter the ingredient to add: ")
            write_to_file(INGREDIENTS_FILE, new_ingredient + '\n')
            print("Ingredient added successfully.")
        elif choice == '2':
            for index, ingredient in enumerate(ingredients, start=1):
                print(f"{index}. {ingredient.strip()}")
            ingredient_index = int(input("Enter ingredient number to edit: ")) - 1
            if 0 <= ingredient_index < len(ingredients):
                new_ingredient = input("Enter the new ingredient name: ")
                ingredients[ingredient_index] = new_ingredient + '\n'
                with open(INGREDIENTS_FILE, "w") as file:
                    file.writelines(ingredients)
                print("Ingredient updated successfully.")
        elif choice == '3':
            for index, ingredient in enumerate(ingredients, start=1):
                print(f"{index}. {ingredient.strip()}")
            ingredient_index = int(input("Enter ingredient number to delete: ")) - 1
            if 0 <= ingredient_index < len(ingredients):
                ingredients.pop(ingredient_index)
                with open(INGREDIENTS_FILE, "w") as file:
                    file.writelines(ingredients)
                print("Ingredient deleted successfully.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def update_chef_profile():
    name = input("Enter new name: ")
    email = input("Enter new email: ")
    phone = input("Enter new phone number: ")
    profile_data = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n"
    write_to_file("chef_profile.txt", profile_data, "w")
    print("Profile updated successfully.")

# Manager Functions for Customer Management
def add_customer():
    name = input("Enter customer name: ")
    contact = input("Enter customer contact: ")
    write_to_file(CUSTOMER_FILE, f"{name},{contact}\n")
    print("Customer added successfully.")

def view_customers():
    customers = read_from_file(CUSTOMER_FILE)
    if customers:
        print("\nCustomer List:")
        for line in customers:
            name, contact = line.strip().split(",")
            print(f"Name: {name}, Contact: {contact}")
    else:
        print("No customers found.")

def edit_customer():
    name = input("Enter customer name to edit: ")
    customers = read_from_file(CUSTOMER_FILE)
    found = False
    new_data = []

    for line in customers:
        customer_name, contact = line.strip().split(",")
        if customer_name == name:
            new_contact = input(f"Enter new contact for {name}: ")
            new_data.append(f"{name},{new_contact}\n")
            found = True
        else:
            new_data.append(line)

    if found:
        with open(CUSTOMER_FILE, "w") as file:
            file.writelines(new_data)
        print(f"Customer '{name}' updated successfully.")
    else:
        print("Customer not found.")

def delete_customer():
    name = input("Enter customer name to delete: ")
    customers = read_from_file(CUSTOMER_FILE)
    new_data = [line for line in customers if not line.startswith(name)]

    if len(customers) != len(new_data):
        with open(CUSTOMER_FILE, "w") as file:
            file.writelines(new_data)
        print(f"Customer '{name}' deleted successfully.")
    else:
        print("Customer not found.")

# Manager Functions for Menu Management
def add_menu_item():
    item = input("Enter menu item name: ")
    price = input("Enter item price: ")
    write_to_file(MENU_FILE, f"{item},{price}\n")
    print("Menu item added successfully.")

def view_menu():
    menu = read_from_file(MENU_FILE)
    if menu:
        print("\nMenu List:")
        for line in menu:
            item, price = line.strip().split(",")
            print(f"Item: {item}, Price: {price}")
    else:
        print("No menu items found.")

def edit_menu_item():
    item = input("Enter menu item name to edit: ")
    menu = read_from_file(MENU_FILE)
    found = False
    new_data = []

    for line in menu:
        menu_item, price = line.strip().split(",")
        if menu_item == item:
            new_price = input(f"Enter new price for {item}: ")
            new_data.append(f"{item},{new_price}\n")
            found = True
        else:
            new_data.append(line)

    if found:
        with open(MENU_FILE, "w") as file:
            file.writelines(new_data)
        print(f"Menu item '{item}' updated successfully.")
    else:
        print("Menu item not found.")

def delete_menu_item():
    item = input("Enter menu item name to delete: ")
    menu = read_from_file(MENU_FILE)
    new_data = [line for line in menu if not line.startswith(item)]

    if len(menu) != len(new_data):
        with open(MENU_FILE, "w") as file:
            file.writelines(new_data)
        print(f"Menu item '{item}' deleted successfully.")
    else:
        print("Menu item not found.")

# Manager Profile Update
def update_manager_profile():
    name = input("Enter your name: ")
    contact = input("Enter your contact: ")
    write_to_file("manager_profile.txt", f"{name},{contact}\n", "w")
    print("Profile updated successfully.")
    
# Manager Functions
def manager_menu():
    while True:
        print("\nManager Menu:")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Edit Customer")
        print("4. Delete Customer")
        print("5. Add Menu Item")
        print("6. View Menu")
        print("7. Edit Menu Item")
        print("8. Delete Menu Item")
        print("9. Update Profile")
        print("0. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_customer()
        elif choice == "2":
            view_customers()
        elif choice == "3":
            edit_customer()
        elif choice == "4":
            delete_customer()
        elif choice == "5":
            add_menu_item()
        elif choice == "6":
            view_menu()
        elif choice == "7":
            edit_menu_item()
        elif choice == "8":
            delete_menu_item()
        elif choice == "9":
            update_manager_profile()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

# Admin Functions
def add_staff():
    name = input("Enter staff name: ")
    position = input("Enter staff position (Manager/Chef/etc.): ")
    write_to_file(STAFF_FILE, f"{name},{position}\n")
    print(f"Added {position}: {name}")

def delete_staff():
    name = input("Enter staff name to delete: ")
    staff = read_from_file(STAFF_FILE)
    new_data = [line for line in staff if not line.startswith(name)]

    if len(staff) != len(new_data):
        with open(STAFF_FILE, "w") as file:
            file.writelines(new_data)
        print(f"Deleted staff: {name}")
    else:
        print("Staff member not found.")

def edit_staff():
    name = input("Enter staff name to edit: ")
    staff = read_from_file(STAFF_FILE)
    found = False
    new_data = []

    for line in staff:
        staff_name, position = line.strip().split(",")
        if staff_name == name:
            new_position = input(f"Enter new position for {name}: ")
            new_data.append(f"{name},{new_position}\n")
            found = True
        else:
            new_data.append(line)

    if found:
        with open(STAFF_FILE, "w") as file:
            file.writelines(new_data)
        print(f"Updated {name} to {new_position}")
    else:
        print("Staff member not found.")

def view_sales_report():
    orders = read_from_file(ORDERS_FILE)
    total_sales = 0
    for order in orders:
        parts = order.strip().split(",")
        order_details = parts[2]
        quantity = int(order_details.split(" x")[1])
        item_name = order_details.split(" x")[0]
        
        # Fetch price from MENU_FILE
        menu = read_from_file(MENU_FILE)
        price = next((float(line.strip().split(",")[1]) for line in menu if line.startswith(item_name)), 0)
        
        total_sales += quantity * price

    print(f"Total Sales: ${total_sales:.2f}")

def view_feedback():
    feedbacks = read_from_file(FEEDBACK_FILE)
    if feedbacks:
        print("\nCustomer Feedback:")
        for feedback in feedbacks:
            customer_id, comments = feedback.strip().split(",", 1)
            print(f"Feedback from {customer_id}: {comments}")
    else:
        print("No feedback available.")

def add_feedback():
    customer_id = input("Enter customer ID: ")
    feedback = input("Enter feedback: ")
    write_to_file(FEEDBACK_FILE, f"{customer_id},{feedback}\n")
    print("Feedback added.")

def update_admin_profile():
    name = input("Enter your name: ")
    contact = input("Enter your contact: ")
    write_to_file("admin_profile.txt", f"{name},{contact}\n", "w")
    print("Profile updated successfully.")

# Admin Functions
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Staff")
        print("2. Delete Staff")
        print("3. Edit Staff")
        print("4. View Sales Report")
        print("5. View Feedback")
        print("6. Add Feedback")
        print("7. Update Profile")
        print("8. Logout")
        choice = input("Select an option: ")
        if choice == '1':
            add_staff()
        elif choice == '2':
            delete_staff()
        elif choice == '3':
            edit_staff()
        elif choice == '4':
            view_sales_report()
        elif choice == '5':
            view_feedback()
        elif choice == '6':
            add_feedback()
        elif choice == '7':
            update_admin_profile()
        elif choice == '8':
            break
        else:
            print("Invalid option, please try again.")

# Main Application
def main():
    while True:
        print("\nWelcome to the Restaurant Management System")
        print("1. Customer")
        print("2. Chef")
        print("3. Manager")
        print("4. Admin")
        print("5. Exit")

        role_choice = input("Enter your choice: ")
        
        if role_choice == "1":
            customer_id = login(CUSTOMER_FILE)
            if customer_id:
                customer_menu(customer_id)
        elif role_choice == "2":
            chef_menu()
        elif role_choice == "3":
            manager_menu()
        elif role_choice == "4":
            admin_menu()
        elif role_choice == "5":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    main()

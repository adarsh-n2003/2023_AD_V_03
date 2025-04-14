import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
import json
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import secrets  # For generating a shorter unique identifier

# Load the pre-trained model
model = load_model('water_detection_model.h5')
credentials_path = 'user_credentials.json'
admin_review_path = 'admin_review.json'

def load_credentials():
    if os.path.exists(credentials_path):
        with open(credentials_path, 'r') as file:
            return json.load(file)
    return {}

def save_credentials(data):
    with open(credentials_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_admin_reviews():
    if os.path.exists(admin_review_path):
        with open(admin_review_path, 'r') as file:
            return json.load(file)
    return {}

def save_admin_reviews(data):
    with open(admin_review_path, 'w') as file:
        json.dump(data, file, indent=4)

user_credentials = load_credentials()
admin_reviews = load_admin_reviews()

def main_screen():
    global main_window
    main_window = tk.Tk()
    main_window.title("Water Detection System")
    main_window.geometry("800x600")

    style = ttk.Style(main_window)
    style.theme_use('clam')
    style.configure('TButton', font=('Arial', 10), padding=5)
    style.configure('TLabel', font=('Arial', 12), padding=5)
    style.configure('TEntry', font=('Arial', 12), padding=5)
    style.configure('TFrame', font=('Arial', 12), padding=5)

    main_frame = ttk.Frame(main_window, padding="10 10 10 10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    username_label = ttk.Label(main_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=5)

    global username_entry
    username_entry = ttk.Entry(main_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = ttk.Label(main_frame, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=5)

    global password_entry
    password_entry = ttk.Entry(main_frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    role_label = ttk.Label(main_frame, text="Role:")
    role_label.grid(row=2, column=0, padx=10, pady=5)

    global role_combobox
    role_combobox = ttk.Combobox(main_frame, values=["User", "Admin"], state="readonly")
    role_combobox.grid(row=2, column=1, padx=10, pady=5)
    role_combobox.current(0)

    login_button = ttk.Button(main_frame, text="Login", command=login_user)
    login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    register_button = ttk.Button(main_frame, text="Register", command=register_user)
    register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    main_window.mainloop()

def login_user():
    username = username_entry.get()
    password = password_entry.get()
    role = role_combobox.get()
    if username in user_credentials and user_credentials[username]['password'] == password and user_credentials[username]['role'] == role:
        global current_user
        current_user = username
        messagebox.showinfo("Success", f"{role} logged in successfully!")
        open_user_admin_page(role)
    else:
        messagebox.showerror("Error", "Invalid username, password, or role!")

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    role = role_combobox.get()
    if username and password and role:
        if username not in user_credentials:
            user_credentials[username] = {'password': password, 'role': role}
            save_credentials(user_credentials)
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def open_user_admin_page(role):
    global main_window
    main_window.destroy()

    if role == "User":
        open_user_page()
    elif role == "Admin":
        open_admin_page()

def open_user_page():
    global user_window
    user_window = tk.Tk()
    user_window.title("User Dashboard")
    user_window.geometry("800x600")

    top_frame = ttk.Frame(user_window, padding="10 10 10 10")
    top_frame.pack(fill=tk.BOTH, expand=True)

    logout_button = ttk.Button(top_frame, text="Logout", command=user_logout)
    logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

    problem_label = ttk.Label(top_frame, text="Describe your Problem:")
    problem_label.pack(fill=tk.X, padx=10, pady=10)

    global problem_text
    problem_text = tk.Text(top_frame, height=3)
    problem_text.pack(fill=tk.X, padx=10, pady=10)

    location_label = ttk.Label(top_frame, text="Location:")
    location_label.pack(fill=tk.X, padx=10, pady=10)

    global location_entry
    location_entry = ttk.Entry(top_frame)
    location_entry.pack(fill=tk.X, padx=10, pady=10)

    upload_button = ttk.Button(top_frame, text="Upload Image", command=upload_image)
    upload_button.pack(padx=10, pady=10)

def user_logout():
    user_window.destroy()
    main_screen()

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        result = check_water(file_path)
        problem = problem_text.get("1.0", "end-1c")
        location = location_entry.get()
        # Save image in the upload folder
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        ticket_number = secrets.token_urlsafe(8)  # Shorter, URL-safe token
        save_image_path = os.path.join('uploads', f"{ticket_number}.png")
        os.replace(file_path, save_image_path)
        if result:
            messagebox.showinfo("Success", f"Your problem has been submitted successfully.\nTicket Number: {ticket_number}")
            send_to_admin(problem, location, save_image_path, ticket_number)
        else:
            messagebox.showinfo("Error", "The uploaded image is not water related.")

def check_water(image_path):
    try:
        # Load and preprocess the image
        image = load_img(image_path, target_size=(150, 150))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0) / 255.0

        # Make prediction
        result = model.predict(image)
        return np.argmax(result) == 0  # Assuming class 0 is for water detection
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image: {str(e)}")
        return False

def send_to_admin(problem, location, image_path, ticket_number):
    # Save ticket details
    admin_reviews[ticket_number] = {'problem': problem, 'location': location, 'image_path': image_path, 'status': 'Pending'}
    save_admin_reviews(admin_reviews)

def open_admin_page():
    global admin_window
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")

    top_frame = ttk.Frame(admin_window, padding="10 10 10 10")
    top_frame.pack(fill=tk.BOTH, expand=True)

    logout_button = ttk.Button(top_frame, text="Logout", command=admin_logout)
    logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

    ticket_tree = ttk.Treeview(top_frame, columns=("Ticket Number", "Location", "Status"), show="headings")
    ticket_tree.pack(fill=tk.BOTH, expand=True)

    ticket_tree.heading("Ticket Number", text="Ticket Number")
    ticket_tree.heading("Location", text="Location")
    ticket_tree.heading("Status", text="Status")
    ticket_tree.bind("<Double-1>", lambda event, tree=ticket_tree: view_ticket_details(event, tree))

    # Populate table with tickets
    for ticket_number, details in admin_reviews.items():
        ticket_tree.insert("", "end", values=(ticket_number, details['location'], details['status']))

def view_ticket_details(event, tree):
    for item in tree.selection():
        item_values = tree.item(item, "values")
        ticket_number = item_values[0]
        details = admin_reviews[ticket_number]
        messagebox.showinfo("Ticket Details", f"Ticket Number: {ticket_number}\nProblem: {details['problem']}\nLocation: {details['location']}\nStatus: {details['status']}\nImage Path: {details['image_path']}")

def admin_logout():
    admin_window.destroy()
    main_screen()

if __name__ == "__main__":
    main_screen()

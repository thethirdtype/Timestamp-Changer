import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os


def set_new_datetime():
    file_path = file_path_var.get()
    new_datetime_str = new_datetime_var.get()

    try:
        new_datetime = datetime.strptime(new_datetime_str, "%Y-%m-%d %H:%M:%S")
        os.utime(file_path, (new_datetime.timestamp(), new_datetime.timestamp()))
        result_label.config(text="Changes saved successfully.")
    except ValueError:
        result_label.config(text="Invalid date and time format. Use yyyy-mm-dd HH:MM:SS.")


def reset_datetime():
    new_datetime_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def process_file(file_path):
    try:
        last_modified_time = os.path.getmtime(file_path)
        last_modified_datetime = datetime.fromtimestamp(last_modified_time)
        new_datetime_var.set(last_modified_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    except OSError:
        result_label.config(text="Error getting file information.")


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_file(file_path)
        file_path_var.set(file_path.replace('/', '\\') if os.name == 'nt' else file_path)


def update_datetime(_event):
    file_path = file_path_var.get()
    if file_path:
        process_file(file_path)
        file_path_var.set(file_path.replace('/', '\\') if os.name == 'nt' else file_path)


# Create main frame
root = tk.Tk()
root.title("Timestamp Changer")

file_path_var = tk.StringVar()
new_datetime_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window width and height
window_width = 320
window_height = 220

# Calculate the x and y coordinates for the Tk root window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Set the window geometry
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Create main frame with additional padding
frame = tk.Frame(root, padx=10)
frame.pack(padx=10, pady=10)

# Add entry for file path
file_path_label = tk.Label(frame, text="Select file:")
file_path_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

file_path_entry = tk.Entry(frame, textvariable=file_path_var, width=30)
file_path_entry.grid(row=1, column=0, columnspan=2)

# Bind the update_datetime function to the FocusOut event of the entry widget
file_path_entry.bind("<FocusOut>", update_datetime)

# Add browse button
browse_button = tk.Button(frame, text="Browse", command=browse_file, width=10)
browse_button.grid(row=1, column=2, padx=(10, 0))

# Add fields for new date and time
new_datetime_label = tk.Label(frame, text="Enter new date and time (yyyy-mm-dd HH:MM:SS):")
new_datetime_label.grid(row=2, column=0, columnspan=3, pady=(10, 5))

new_datetime_entry = tk.Entry(frame, textvariable=new_datetime_var, width=30)
new_datetime_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))

# Add button to reset to current date and time
reset_button = tk.Button(frame, text="Now", command=reset_datetime, width=10)
reset_button.grid(row=3, column=2, padx=(10, 0))

# Add button to save changes
save_button = tk.Button(frame, text="Save Changes", command=set_new_datetime, width=20)
save_button.grid(row=4, column=0, columnspan=3, pady=(15, 0))

# Display result label
result_label = tk.Label(frame, text="")
result_label.grid(row=5, column=0, columnspan=3, pady=(10, 0))

# Set Icon
root.iconbitmap("tc_icon.ico")

# Run the Tkinter event loop
root.mainloop()

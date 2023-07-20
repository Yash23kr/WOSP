import os
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

def identify_file_types(directory):
    file_types = {}
    total_files = 0
    total_size = 0
    largest_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            file_extension = os.path.splitext(file)[1][1:].lower()
            file_types[file_extension] = file_types.get(file_extension, 0) + 1
            largest_files.append((file_path, file_size))
    largest_files.sort(key=lambda x: x[1], reverse=True)
    return file_types, total_files, total_size, largest_files

def delete_files_of_type(directory, file_type):
    deleted_files = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith("." + file_type):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files += 1
                except Exception as e:
                    pass
    return deleted_files

def browse_directory():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_types, total_files, total_size, largest_files = identify_file_types(folder_path)
        types_label.config(text="File Types Found:")
        types = format_file_types(file_types.keys())
        types_text.config(state=tk.NORMAL)
        types_text.delete(1.0, tk.END)
        types_text.insert(tk.END, types)
        types_text.config(state=tk.DISABLED)

        total_files_label.config(text="Total Files: " + str(total_files))
        total_size_label.config(text="Total Size: " + format_size(total_size))

        # Create and display the bar graph
        plt.bar(file_types.keys(), file_types.values())
        plt.xlabel("File Types")
        plt.ylabel("Number of Files")
        plt.title("Number of Files of Different Types")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # Display Largest Files
        largest_files_label.config(text="Largest Files:")
        largest_files_listbox.delete(0, tk.END)
        for file_path, file_size in largest_files[:10]:
            largest_files_listbox.insert(tk.END, f"{format_size(file_size)} - {file_path}")

def delete_files():
    directory = directory_var.get()
    file_type = file_type_entry.get().strip().lower()
    
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory path!")
        return
    
    if file_type == "":
        messagebox.showerror("Error", "Please enter a file type!")
        return

    deleted_files = delete_files_of_type(directory, file_type)
    messagebox.showinfo("Deletion Complete", f"Deleted {deleted_files} files of type: {file_type}.")

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0

def format_file_types(file_types):
    types = list(file_types)
    formatted_types = [", ".join(types[i:i+10]) for i in range(0, len(types), 10)]
    return "\n".join(formatted_types)

# GUI
root = tk.Tk()
root.title("File Type Deletion")

directory_var = tk.StringVar()

select_label = tk.Label(root, text="Select a directory:")
select_label.pack()

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack()

types_label = tk.Label(root, text="File Types Found:")
types_label.pack()

types_text = tk.Text(root, height=5, width=50, state=tk.DISABLED)
types_text.pack()

total_files_label = tk.Label(root, text="Total Files: ")
total_files_label.pack()

total_size_label = tk.Label(root, text="Total Size: ")
total_size_label.pack()

file_type_entry = tk.Entry(root)
file_type_entry.pack()

delete_button = tk.Button(root, text="Delete Files", command=delete_files)
delete_button.pack()

# Largest Files
largest_files_label = tk.Label(root, text="Largest Files:")
largest_files_label.pack()

largest_files_listbox = tk.Listbox(root, height=10, width=100)
largest_files_listbox.pack()

root.mainloop()

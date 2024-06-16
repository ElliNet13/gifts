import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile

# Function to create user-specific directories
def create_user_dirs():
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    user_folder = os.path.join(base_folder, user_name)
    if not os.path.exists(user_folder):
        os.mkdir(user_folder)
        os.mkdir(os.path.join(user_folder, 'unopened'))
        os.mkdir(os.path.join(user_folder, 'opened'))

# Function to display main menu
def main_menu():
    while True:
        clear_screen()
        print("===========================")
        print("     Gifts Application")
        print("===========================")
        print()
        print("1. Check for gifts")
        print("2. Open a gift")
        print("3. View opened gifts")
        print("4. Send a gift")
        print("5. Create a gift")
        print("6. Exit")
        print()

        choice = input("Choose an option: ")

        # Process user choice
        if choice == '1':
            check_gifts()
        elif choice == '2':
            open_gift()
        elif choice == '3':
            view_opened()
        elif choice == '4':
            send_gift_gui()
        elif choice == '5':
            create_gift()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to check for unopened gifts
def check_gifts():
    clear_screen()
    print("===========================")
    print("     Unopened Gifts")
    print("===========================")
    print()

    user_folder_unopened = os.path.join(base_folder, user_name, 'unopened')
    gifts = os.listdir(user_folder_unopened)

    if not gifts:
        print("No gifts available.")
    else:
        for i, gift in enumerate(gifts, 1):
            print(f"{i}. {os.path.splitext(gift)[0]}")

    input("Press Enter to continue...")

# Function to open a gift
def open_gift():
    clear_screen()
    print("===========================")
    print("     Open a Gift")
    print("===========================")
    print()

    user_folder_unopened = os.path.join(base_folder, user_name, 'unopened')
    gifts = os.listdir(user_folder_unopened)

    if not gifts:
        print("No gifts available.")
        input("Press Enter to continue...")
        return

    for i, gift in enumerate(gifts, 1):
        print(f"{i}. {os.path.splitext(gift)[0]}")

    choice = input("Enter the number of the gift you want to open: ")

    try:
        choice = int(choice)
        if choice < 1 or choice > len(gifts):
            raise ValueError
    except ValueError:
        print("Invalid choice. Please enter a number.")
        input("Press Enter to continue...")
        return

    selected_gift = os.path.join(user_folder_unopened, gifts[choice - 1])
    gift_name = os.path.splitext(gifts[choice - 1])[0]

    print(f"Opening gift: {gift_name}")

    opened_folder = os.path.join(base_folder, user_name, 'opened', gift_name)
    os.makedirs(opened_folder, exist_ok=True)
    os.rename(selected_gift, os.path.join(opened_folder, f"{gifts[choice - 1]}"))

    onopened_file = os.path.join(opened_folder, 'onopened.txt')
    if os.path.exists(onopened_file):
        with open(onopened_file, 'r') as f:
            app_to_launch = f.read().strip()
            print(f"Opening {app_to_launch}...")
            # Implement launching the application here if desired

    input("Press Enter to continue...")

# Function to view opened gifts
def view_opened():
    clear_screen()
    print("===========================")
    print("     Opened Gifts")
    print("===========================")
    print()

    user_folder_opened = os.path.join(base_folder, user_name, 'opened')
    gifts = os.listdir(user_folder_opened)

    if not gifts:
        print("No opened gifts available.")
    else:
        for i, gift in enumerate(gifts, 1):
            print(f"{i}. {gift}")

    input("Press Enter to continue...")

# Function to send a gift using GUI file picker
def send_gift_gui():
    clear_screen()
    print("===========================")
    print("     Send a Gift")
    print("===========================")
    print()

    recipient = input("Enter the recipient's username (no spaces): ")

    recipient_folder = os.path.join(base_folder, recipient)
    if not os.path.exists(recipient_folder):
        print(f"Error: Recipient '{recipient}' does not exist.")
        input("Press Enter to continue...")
        return

    root = tk.Tk()
    # root.withdraw()  # Commented out to keep the GUI visible

    file_path = filedialog.askopenfilename(title="Select a .zip file to send")
    root.destroy()

    if not file_path:
        print("No file selected.")
        input("Press Enter to continue...")
        return

    if not file_path.lower().endswith('.zip'):
        print("Error: Only .zip files can be sent as gifts.")
        input("Press Enter to continue...")
        return

    shutil.move(file_path, os.path.join(recipient_folder, 'unopened', os.path.basename(file_path)))
    print(f"Gift sent successfully to {recipient}.")
    input("Press Enter to continue...")

# Function to create a gift using GUI interface
def create_gift():
    clear_screen()
    print("===========================")
    print("     Create a Gift")
    print("===========================")
    print()

    root = tk.Tk()
    # root.withdraw()  # Commented out to keep the GUI visible

    app = GiftCreatorApp(root)
    root.mainloop()

# Gift Creator GUI class
class GiftCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gift Creator")
        self.root.geometry("500x400")

        self.files_to_include = []
        self.main_file = None

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)

        # Add Files button
        btn_add_files = tk.Button(frame_buttons, text="Add Files", command=self.add_files)
        btn_add_files.pack(side=tk.LEFT, padx=10)

        # Main File button
        btn_main_file = tk.Button(frame_buttons, text="Select Main File", command=self.select_main_file)
        btn_main_file.pack(side=tk.LEFT, padx=10)

        # Done button
        btn_done = tk.Button(frame_buttons, text="Done", command=self.create_zip)
        btn_done.pack(side=tk.LEFT, padx=10)

        # Listbox to display added files
        self.list_files = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=60)
        self.list_files.pack(pady=20)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files to include in the gift")
        if files:
            for file in files:
                if file not in self.files_to_include:
                    self.files_to_include.append(file)
                    self.list_files.insert(tk.END, os.path.basename(file))

    def select_main_file(self):
        if not self.files_to_include:
            messagebox.showwarning("Warning", "Please add files first.")
            return

        self.main_file = filedialog.askopenfilename(title="Select the main file to launch")
        if self.main_file and self.main_file not in self.files_to_include:
            messagebox.showinfo("Main File Selected", f"Main File: {os.path.basename(self.main_file)}")

    def create_zip(self):
        if not self.files_to_include:
            messagebox.showwarning("Warning", "Please add files first.")
            return

        if not self.main_file:
            messagebox.showwarning("Warning", "Please select a main file.")
            return

        zip_filename = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            title="Save Gift As"
        )

        if zip_filename:
            try:
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for file in self.files_to_include:
                        zipf.write(file, os.path.basename(file))

                with open(os.path.join(os.path.dirname(zip_filename), 'onopened.txt'), 'w') as f:
                    f.write(os.path.basename(self.main_file))

                messagebox.showinfo("Gift Created", f"Gift created successfully: {zip_filename}")
                self.root.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Error creating gift: {e}")

def main():
    global base_folder, user_name
    base_folder = os.path.join(os.getcwd(), 'GiftsApp')

    # Create GiftsApp folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    clear_screen()
    print("Welcome to Gifts Application!")
    user_name = input("Enter your username (no spaces): ")

    create_user_dirs()
    main_menu()

if __name__ == "__main__":
    main()
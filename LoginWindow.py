from tkinter import *
from Utils import Utils
from ErrorModel import ErrorModel
from Organisation import Organisation
from NoSuchUserException import NoSuchUserException


class LoginWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Warehouse Login")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", Utils.disable)

        # Main container
        self.container = Frame(self.root)
        self.container.pack(padx=20, pady=20)

        # Header
        self.header = Utils.Label(self.container, "Login to Warehouse System")
        self.header.pack(pady=(0, 20))

        # Username field
        self.username_label = Label(self.container, text="Username:", font="Arial 11")
        self.username_label.pack(fill=X)
        self.username_entry = Entry(self.container, font="Arial 11")
        self.username_entry.pack(fill=X, pady=(0, 10))

        # Password field
        self.password_label = Label(self.container, text="Password:", font="Arial 11")
        self.password_label.pack(fill=X)
        self.password_entry = Entry(self.container, show="*", font="Arial 11")
        self.password_entry.pack(fill=X, pady=(0, 20))

        # Login button
        self.login_button = Utils.Button(self.container, "Login", self.login)
        self.login_button.pack(fill=X)

        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_error(self, error_model):
        error_window = Toplevel(self.root)
        error_window.title("Error")
        error_window.resizable(False, False)

        container = Frame(error_window)
        container.pack(padx=20, pady=20)

        message_label = Label(container, text=error_model.message, font="Arial 11")
        message_label.pack(pady=(0, 10))

        ok_button = Utils.Button(container, "OK", error_window.destroy)
        ok_button.pack(fill=X)

        error_window.transient(self.root)
        error_window.grab_set()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            organisation = Organisation()
            user = organisation.users.validate_user(username, password)
            Organisation.logged_in_user = user
            self.root.destroy()
            # Here we would launch the appropriate dashboard based on user type
            from UserDashboard import UserDashboard
            UserDashboard()
        except NoSuchUserException:
            self.show_error(ErrorModel(
                NoSuchUserException(),
                "Invalid username or password"
            ))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    login = LoginWindow()
    login.run()
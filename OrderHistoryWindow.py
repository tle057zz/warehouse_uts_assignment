from tkinter import *
from Utils import Utils
from Organisation import Organisation


class OrderHistoryWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Order History")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", Utils.disable)

        # Main container
        self.container = Frame(self.root)
        self.container.pack(padx=20, pady=20)

        # Header
        self.header = Utils.Label(self.container, "Your Order History")
        self.header.pack(pady=(0, 20))

        # Order history ListView
        self.history_listbox = Listbox(self.container, font="Arial 11")
        self.history_listbox.pack(fill=X, pady=(0, 20))

        # Populate order history
        user = Organisation.logged_in_user
        for purchase in user.purchases:
            self.history_listbox.insert(END, str(purchase))

        # Back button
        self.back_button = Utils.Button(self.container, "Back", self.go_back)
        self.back_button.pack(fill=X)

        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.mainloop()

    def go_back(self):
        self.root.destroy()
        from UserDashboard import UserDashboard
        UserDashboard()
from tkinter import *
from Utils import Utils
from Organisation import Organisation
from Manager import Manager


class UserDashboard:
    def __init__(self):
        self.root = Tk()
        self.root.title("Warehouse Dashboard")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", Utils.disable)

        # Main container
        self.container = Frame(self.root)
        self.container.pack(padx=20, pady=20)

        # Welcome message
        user_type = "Manager" if isinstance(Organisation.logged_in_user, Manager) else "User"
        welcome_text = f"Welcome {Organisation.logged_in_user.get_full_name()} ({user_type})"
        self.welcome_label = Utils.Label(self.container, welcome_text)
        self.welcome_label.pack(pady=(0, 20))

        # Buttons
        self.shop_button = Utils.Button(self.container, "Shop", self.open_supplier_list)
        self.shop_button.pack(fill=X, pady=(0, 10))

        self.history_button = Utils.Button(self.container, "Order History", self.open_order_history)
        self.history_button.pack(fill=X, pady=(0, 10))

        # Manager-specific button
        if isinstance(Organisation.logged_in_user, Manager):
            self.manage_button = Utils.Button(self.container, "Manage", self.open_manager_view)
            self.manage_button.pack(fill=X, pady=(0, 10))

        self.close_button = Utils.Button(self.container, "Close", self.close_application)
        self.close_button.pack(fill=X)

        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.mainloop()

    def open_supplier_list(self):
        self.root.destroy()
        # Import here to avoid circular imports
        from SupplierListWindow import SupplierListWindow
        SupplierListWindow()

    def open_order_history(self):
        self.root.destroy()
        from OrderHistoryWindow import OrderHistoryWindow
        OrderHistoryWindow()

    def open_manager_view(self):
        self.root.destroy()
        from ManagerDashboard import ManagerDashboard
        ManagerDashboard()

    def close_application(self):
        self.root.quit()
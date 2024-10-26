from tkinter import *
from tkinter import ttk
from Utils import Utils
from Organisation import Organisation


class ManagerDashboard:
    def __init__(self):
        self.root = Tk()
        self.root.title("Manager Dashboard")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", Utils.disable)

        # Main container
        self.container = Frame(self.root)
        self.container.pack(padx=20, pady=20)

        # Header
        manager = Organisation.logged_in_user
        self.header = Utils.Label(self.container, f"Managing Suppliers for {manager.get_full_name()}")
        self.header.pack(pady=(0, 20))

        # Supplier Table
        self.tree = ttk.Treeview(self.container, columns=("Name", "Region", "Products"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Region", text="Region")
        self.tree.heading("Products", text="Products")
        self.tree.pack(fill=X, pady=(0, 20))

        # Populate suppliers
        for supplier in manager.suppliers.suppliers:
            product_count = len(supplier.products.get_all_products())
            self.tree.insert("", END, values=(supplier.name, supplier.region, f"{product_count} items"))

        # Filter frame
        self.filter_frame = Frame(self.container)
        self.filter_frame.pack(fill=X, pady=(0, 20))

        self.filter_var = BooleanVar()
        self.filter_check = Checkbutton(self.filter_frame, text="Show only available products",
                                        variable=self.filter_var, command=self.filter_products)
        self.filter_check.pack(side=LEFT)

        # Buttons frame
        self.buttons_frame = Frame(self.container)
        self.buttons_frame.pack(fill=X)

        self.remove_button = Utils.Button(self.buttons_frame, "Remove", self.remove_product)
        self.remove_button.pack(fill=X, pady=(0, 10))

        self.delist_button = Utils.Button(self.buttons_frame, "Delist", self.delist_product)
        self.delist_button.pack(fill=X, pady=(0, 10))

        self.back_button = Utils.Button(self.buttons_frame, "Back", self.go_back)
        self.back_button.pack(fill=X)

        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.mainloop()

    def filter_products(self):
        # Implement product filtering logic
        pass

    def remove_product(self):
        # Implement product removal logic
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def delist_product(self):
        # Implement product delisting logic
        pass

    def go_back(self):
        self.root.destroy()
        from UserDashboard import UserDashboard
        UserDashboard()
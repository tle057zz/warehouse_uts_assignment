from tkinter import *
from tkinter import ttk
from Utils import Utils
from Organisation import Organisation


class SupplierListWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Supplier List")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", Utils.disable)

        # Main container
        self.container = Frame(self.root)
        self.container.pack(padx=20, pady=20)

        # Header
        self.header = Utils.Label(self.container, "Select a Supplier")
        self.header.pack(pady=(0, 20))

        # Supplier ListView
        self.supplier_listbox = Listbox(self.container, font="Arial 11", selectmode=SINGLE)
        self.supplier_listbox.pack(fill=X, pady=(0, 20))

        # Add scrollbar
        scrollbar = Scrollbar(self.container, orient=VERTICAL)
        scrollbar.config(command=self.supplier_listbox.yview)
        self.supplier_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Populate suppliers
        organisation = Organisation()
        for supplier in organisation.suppliers.suppliers:
            self.supplier_listbox.insert(END, f"{supplier.name} - {supplier.region}")

        # Buttons frame
        self.buttons_frame = Frame(self.container)
        self.buttons_frame.pack(fill=X)

        # Shop button
        self.shop_button = Utils.Button(self.buttons_frame, "Shop", self.open_supplier_dashboard)
        self.shop_button.pack(fill=X, pady=(0, 10))

        # Back button
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

    def open_supplier_dashboard(self):
        selection = self.supplier_listbox.curselection()
        if selection:
            self.root.destroy()
            from SupplierDashboard import SupplierDashboard
            supplier_idx = selection[0]
            organisation = Organisation()
            selected_supplier = organisation.suppliers.suppliers[supplier_idx]
            SupplierDashboard(selected_supplier)

    def go_back(self):
        self.root.destroy()
        from UserDashboard import UserDashboard
        UserDashboard()


if __name__ == "__main__":
    # For testing purposes
    SupplierListWindow()
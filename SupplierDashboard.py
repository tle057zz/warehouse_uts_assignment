from tkinter import *
from tkinter import ttk
from Utils import Utils
from Organisation import Organisation
from Cart import Cart
from Order import Order
from InvalidQuantityException import InvalidQuantityException
from ErrorModel import ErrorModel


class SupplierDashboard:
    def __init__(self, supplier):
        self.root = Tk()
        self.root.title(f"Supplier - {supplier.name}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", Utils.disable)

        self.supplier = supplier
        self.cart = Cart(supplier, Organisation.logged_in_user)

        # Main container
        self.container = Frame(self.root)
        self.container.pack(padx=20, pady=20)

        # Header
        self.header = Utils.Label(self.container, f"Products from {supplier.name} ({supplier.region})")
        self.header.pack(pady=(0, 20))

        # Products Table
        self.tree = ttk.Treeview(self.container, columns=("Name", "Price", "Stock", "Available"),
                                 show="headings", selectmode="extended")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Available", text="Available")
        self.tree.pack(fill=X, pady=(0, 20))

        # Populate products from catalogue
        for product in self.cart.catalogue:
            self.tree.insert("", END, values=(
                product.name,
                f"${product.price:.2f}",
                product.stock,
                "Yes" if product.is_available() else "No"
            ))

        # Buttons frame
        self.buttons_frame = Frame(self.container)
        self.buttons_frame.pack(fill=X)

        self.order_button = Utils.Button(self.buttons_frame, "Order", self.open_quantity_dialog)
        self.order_button.pack(fill=X, pady=(0, 10))

        self.view_cart_button = Utils.Button(self.buttons_frame, "View Cart", self.view_cart)
        self.view_cart_button.pack(fill=X, pady=(0, 10))

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

    def open_quantity_dialog(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        dialog = Toplevel(self.root)
        dialog.title("Enter Quantity")
        dialog.resizable(False, False)

        container = Frame(dialog)
        container.pack(padx=20, pady=20)

        quantity_label = Label(container, text="Quantity:", font="Arial 11")
        quantity_label.pack(fill=X)

        quantity_entry = Entry(container, font="Arial 11")
        quantity_entry.pack(fill=X, pady=(0, 10))

        def add_to_cart():
            try:
                quantity = int(quantity_entry.get())
                if quantity < 1:
                    raise InvalidQuantityException()

                for item_id in selected_items:
                    item = self.tree.item(item_id)
                    values = item['values']
                    product_name = values[0]

                    # Find product in catalogue
                    product = next(p for p in self.cart.catalogue if p.name == product_name)

                    # Add to cart
                    order = Order(product, quantity, self.cart)
                    self.cart.add_order(order)

                    # Remove from tree
                    self.tree.delete(item_id)

                dialog.destroy()

            except ValueError:
                self.show_error(ErrorModel(ValueError(), "Please enter a valid number"))
            except InvalidQuantityException:
                self.show_error(ErrorModel(InvalidQuantityException(), "Invalid quantity entered"))

        confirm_button = Utils.Button(container, "Add to Cart", add_to_cart)
        confirm_button.pack(fill=X)

        dialog.transient(self.root)
        dialog.grab_set()

    def view_cart(self):
        cart_window = Toplevel(self.root)
        cart_window.title("Shopping Cart")
        cart_window.resizable(False, False)

        container = Frame(cart_window)
        container.pack(padx=20, pady=20)

        # Cart items table
        tree = ttk.Treeview(container, columns=("Product", "Quantity", "Cost"), show="headings")
        tree.heading("Product", text="Product")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Cost", text="Cost")
        tree.pack(fill=X, pady=(0, 20))

        # Populate cart items
        for order in self.cart.orders:
            tree.insert("", END, values=(
                order.product.name,
                order.quantity,
                f"${order.get_profit():.2f}"
            ))

        # Total cost
        total_label = Label(container,
                            text=f"Total Cost: ${self.cart.get_total_cost():.2f}",
                            font="Arial 11 bold")
        total_label.pack(pady=(0, 20))

        # Buttons
        buttons_frame = Frame(container)
        buttons_frame.pack(fill=X)

        remove_button = Utils.Button(buttons_frame, "Remove",
                                     lambda: self.remove_from_cart(tree, cart_window))
        remove_button.pack(fill=X, pady=(0, 10))

        checkout_button = Utils.Button(buttons_frame, "Checkout",
                                       lambda: self.checkout(cart_window))
        checkout_button.pack(fill=X, pady=(0, 10))

        cancel_button = Utils.Button(buttons_frame, "Cancel", cart_window.destroy)
        cancel_button.pack(fill=X)

        cart_window.transient(self.root)
        cart_window.grab_set()

    def remove_from_cart(self, tree, cart_window):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])
            product_name = item['values'][0]

            # Find order in cart
            order = next(o for o in self.cart.orders if o.product.name == product_name)
            self.cart.remove_order(order)

            # Add product back to main tree
            self.tree.insert("", END, values=(
                order.product.name,
                f"${order.product.price:.2f}",
                order.product.stock,
                "Yes" if order.product.is_available() else "No"
            ))

            # Remove from cart tree
            tree.delete(selected_item)

            # Update total cost
            for widget in cart_window.winfo_children():
                if isinstance(widget, Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, Label) and "Total Cost" in child['text']:
                            child.config(text=f"Total Cost: ${self.cart.get_total_cost():.2f}")

    def checkout(self, cart_window):
        if self.cart.orders:
            self.supplier.process_cart(self.cart)
            Organisation.logged_in_user.add_purchase(self.cart)
            cart_window.destroy()
            self.go_back()

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

    def go_back(self):
        self.root.destroy()
        from SupplierListWindow import SupplierListWindow
        SupplierListWindow()
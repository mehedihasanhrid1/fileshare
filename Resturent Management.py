import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import os

TAX_RATE = 1.065
MENU_FILE = "menu.txt"
SALES_FILE = "sales.txt"

class RestaurantManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.root.geometry("950x600")
        self.root.configure(bg="#f0f4f8")

        self.qty_vars = {}
        self.qty_widgets = {}
        self.menu = {}
        self.load_menu()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.order_tab = ttk.Frame(self.notebook)
        self.item_tab = ttk.Frame(self.notebook)
        self.sales_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.order_tab, text="Order")
        self.notebook.add(self.item_tab, text="  Item Management")
        self.notebook.add(self.sales_tab, text=" Sales History")

        self.build_order_tab()
        self.build_item_tab()
        self.build_sales_tab()

    def load_menu(self):
        self.menu.clear()
        if not os.path.exists(MENU_FILE):
            open(MENU_FILE, "w").close()
        with open(MENU_FILE) as f:
            for line in f:
                if line.strip():
                    n, p, s = line.strip().split("|")
                    self.menu[n] = [float(p), int(s)]

    def save_menu(self):
        with open(MENU_FILE, "w") as f:
            for k, v in self.menu.items():
                f.write(f"{k}|{v[0]}|{v[1]}\n")

    # ================= ORDER TAB =================

    def build_order_tab(self):
        ttk.Label(self.order_tab, text="Customer Name", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.order_tab, text="Phone", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.customer_name = ttk.Entry(self.order_tab, width=25, font=("Arial", 12))
        self.customer_phone = ttk.Entry(self.order_tab, width=20, font=("Arial", 12))

        self.customer_name.grid(row=0, column=1, padx=5)
        self.customer_phone.grid(row=0, column=3, padx=5)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#004080")
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        self.tree = ttk.Treeview(
            self.order_tab,
            columns=("Item", "Price", "Stock", "Qty"),
            show="headings",
            height=12
        )

        for c in ("Item", "Price", "Stock", "Qty"):
            self.tree.heading(c, text=c)

        self.tree.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        self.total_label = tk.Label(self.order_tab, text="Total: BDT 0.00", font=("Arial", 16, "bold"), fg="#d9534f", bg="#f0f4f8")
        self.total_label.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(self.order_tab, text="Calculate Total", command=self.calculate_total, width=18).grid(row=2, column=0, pady=5, padx=5)
        ttk.Button(self.order_tab, text="Place Order", command=self.place_order, width=18).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(self.order_tab, text="Clear", command=self.refresh_tree, width=18).grid(row=2, column=2, pady=5, padx=5)

        self.refresh_tree()

    def refresh_tree(self):
        for w in self.qty_widgets.values():
            w.destroy()
        self.qty_widgets.clear()
        self.qty_vars.clear()

        for r in self.tree.get_children():
            self.tree.delete(r)

        for item, (price, stock) in self.menu.items():
            self.tree.insert("", tk.END, iid=item, values=(item, price, stock, ""))

        self.root.after(100, self.attach_qty_inputs)
        self.total_label.config(text="Total: BDT 0.00")

    def attach_qty_inputs(self):
        for item in self.menu:
            if item in self.qty_widgets:
                continue
            box = self.tree.bbox(item, "#4")
            if not box:
                self.root.after(50, self.attach_qty_inputs)
                return
            x, y, w, h = box
            var = tk.IntVar(value=0)
            spin = ttk.Spinbox(self.tree, from_=0, to=99, textvariable=var, width=5, font=("Arial", 10))
            spin.place(x=x+2, y=y+2, width=w-4, height=h-4)
            self.qty_vars[item] = var
            self.qty_widgets[item] = spin

    def calculate_total(self):
        total = 0
        for item, var in self.qty_vars.items():
            total += var.get() * self.menu[item][0]
        self.total_label.config(text=f"Total: BDT {total:.2f}")

    def place_order(self):
        if not self.customer_name.get() or not self.customer_phone.get():
            messagebox.showerror("Error", "Customer details required")
            return

        today = date.today().isoformat()
        records = []
        total = 0

        for item, var in self.qty_vars.items():
            qty = var.get()
            if qty > 0:
                if qty > self.menu[item][1]:
                    messagebox.showerror("Error", f"Insufficient stock: {item}")
                    return
                price = self.menu[item][0]
                cost = qty * price
                self.menu[item][1] -= qty
                total += cost
                records.append((today, self.customer_name.get(), self.customer_phone.get(), item, qty, price, cost))

        if not records:
            messagebox.showerror("Error", "No items selected")
            return

        with open(SALES_FILE, "a") as f:
            for r in records:
                f.write("|".join(map(str, r)) + "\n")

        self.save_menu()
        self.refresh_tree()
        self.load_sales()
        messagebox.showinfo("Success", f"Total Bill: BDT {total:.2f}")

    # ================= ITEM MANAGEMENT =================

    def build_item_tab(self):
        ttk.Label(self.item_tab, text="Add New Item", font=("Arial", 14, "bold"), foreground="#004080").grid(row=0, column=0, pady=5, sticky="w")

        ttk.Label(self.item_tab, text="Name", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
        ttk.Label(self.item_tab, text="Base Price", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
        ttk.Label(self.item_tab, text="Stock", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w")

        self.new_name = ttk.Entry(self.item_tab, font=("Arial", 12))
        self.new_price = ttk.Entry(self.item_tab, font=("Arial", 12))
        self.new_stock = ttk.Entry(self.item_tab, font=("Arial", 12))

        self.new_name.grid(row=1, column=1, padx=5)
        self.new_price.grid(row=2, column=1, padx=5)
        self.new_stock.grid(row=3, column=1, padx=5)

        ttk.Button(self.item_tab, text="Add New Item", command=self.add_new_item, width=20).grid(row=4, column=1, pady=5)

        ttk.Separator(self.item_tab, orient=tk.HORIZONTAL).grid(row=5, columnspan=3, sticky="ew", pady=10)

        ttk.Label(self.item_tab, text="Update Existing Item", font=("Arial", 14, "bold"), foreground="#004080").grid(row=6, column=0, sticky="w")

        ttk.Label(self.item_tab, text="Select Item", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky="w")
        self.item_select = ttk.Combobox(self.item_tab, values=list(self.menu.keys()), state="readonly", font=("Arial", 12))
        self.item_select.grid(row=7, column=1, padx=5)
        self.item_select.bind("<<ComboboxSelected>>", self.load_item_data)

        ttk.Label(self.item_tab, text="Price", font=("Arial", 12, "bold")).grid(row=8, column=0, sticky="w")
        ttk.Label(self.item_tab, text="Stock", font=("Arial", 12, "bold")).grid(row=9, column=0, sticky="w")

        self.up_price = ttk.Entry(self.item_tab, font=("Arial", 12))
        self.up_stock = ttk.Entry(self.item_tab, font=("Arial", 12))

        self.up_price.grid(row=8, column=1, padx=5)
        self.up_stock.grid(row=9, column=1, padx=5)

        ttk.Button(self.item_tab, text="Update Item", command=self.update_item, width=20).grid(row=10, column=1, pady=5)

    def add_new_item(self):
        try:
            name = self.new_name.get().strip()
            if not name:
                messagebox.showerror("Error", "Item name cannot be empty")
                return
            if name in self.menu:
                messagebox.showerror("Error", f"Item '{name}' already exists")
                return

            price = round(float(self.new_price.get()) * TAX_RATE, 2)
            stock = int(self.new_stock.get())

            self.menu[name] = [price, stock]
            self.save_menu()
            self.refresh_tree()
            self.item_select["values"] = list(self.menu.keys())

            # Clear the input fields
            self.new_name.delete(0, tk.END)
            self.new_price.delete(0, tk.END)
            self.new_stock.delete(0, tk.END)

            messagebox.showinfo("Success", f"Item '{name}' added successfully!")

        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")


    def load_item_data(self, event):
        item = self.item_select.get()
        price, stock = self.menu[item]
        self.up_price.delete(0, tk.END)
        self.up_stock.delete(0, tk.END)
        self.up_price.insert(0, price)
        self.up_stock.insert(0, stock)

    def update_item(self):
        try:
            item = self.item_select.get()
            if not item:
                messagebox.showerror("Error", "No item selected")
                return

            if self.up_price.get():
                self.menu[item][0] = round(float(self.up_price.get()), 2)
            if self.up_stock.get():
                self.menu[item][1] = int(self.up_stock.get())

            self.save_menu()
            self.refresh_tree()

            messagebox.showinfo("Success", f"Item '{item}' updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid update data: {e}")


    # ================= SALES =================

    def build_sales_tab(self):
        style = ttk.Style()
        style.configure("Sales.Treeview.Heading", font=("Arial", 12, "bold"), foreground="#004080")
        style.configure("Sales.Treeview", font=("Arial", 11), rowheight=25)

        columns = ("Date", "Customer", "Phone", "Item", "Qty", "Price", "Total")
        self.sales_tree = ttk.Treeview(self.sales_tab, columns=columns, show="headings", height=20, style="Sales.Treeview")
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, anchor="center", width=100)

        self.sales_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_sales()

    def load_sales(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        if os.path.exists(SALES_FILE):
            with open(SALES_FILE) as f:
                for line in f:
                    if line.strip():
                        today, name, phone, item, qty, price, cost = line.strip().split("|")
                        self.sales_tree.insert("", tk.END, values=(today, name, phone, item, qty, price, cost))

        # Optional: alternate row colors for readability
        for i, row in enumerate(self.sales_tree.get_children()):
            if i % 2 == 0:
                self.sales_tree.item(row, tags=("evenrow",))
            else:
                self.sales_tree.item(row, tags=("oddrow",))

        self.sales_tree.tag_configure("evenrow", background="#f0f4f8")
        self.sales_tree.tag_configure("oddrow", background="#ffffff")

if __name__ == "__main__":
    root = tk.Tk()
    RestaurantManagementSystem(root)
    root.mainloop()

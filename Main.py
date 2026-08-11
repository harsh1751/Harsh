"""
Inventory Management System
----------------------------
A simple console-based Inventory Management System built using a Python
dictionary as the core data structure.

Data structure:
    inventory = {
        "item_id": {
            "name": str,
            "quantity": int,
            "price": float,
            "category": str
        },
        ...
    }

Features:
    1. Add a new item
    2. View all items
    3. Search for an item
    4. Update an item (quantity / price / category / name)
    5. Delete an item
    6. Low stock report
    7. Total inventory value
    8. Save inventory to file (JSON)
    9. Load inventory from file (JSON)
    0. Exit
"""

import json
import os

DATA_FILE = "inventory_data.json"
LOW_STOCK_THRESHOLD = 5


class InventoryManager:
    def __init__(self):
        # Core data structure: dictionary of dictionaries
        self.inventory = {}

    # ---------------------------------------------------------------
    # CRUD operations
    # ---------------------------------------------------------------
    def add_item(self, item_id, name, quantity, price, category):
        if item_id in self.inventory:
            print(f"⚠️  Item ID '{item_id}' already exists. Use update instead.")
            return
        self.inventory[item_id] = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "category": category,
        }
        print(f"✅ Item '{name}' added successfully.")

    def view_all_items(self):
        if not self.inventory:
            print("📭 Inventory is empty.")
            return

        header = f"{'ID':<10}{'Name':<20}{'Qty':<8}{'Price':<10}{'Category':<15}"
        print(header)
        print("-" * len(header))
        for item_id, details in self.inventory.items():
            print(
                f"{item_id:<10}{details['name']:<20}{details['quantity']:<8}"
                f"${details['price']:<9.2f}{details['category']:<15}"
            )

    def search_item(self, key):
        """Search by item_id or by (partial, case-insensitive) name."""
        results = {}

        if key in self.inventory:
            results[key] = self.inventory[key]

        for item_id, details in self.inventory.items():
            if key.lower() in details["name"].lower() and item_id not in results:
                results[item_id] = details

        if not results:
            print(f"🔍 No items found matching '{key}'.")
            return

        for item_id, details in results.items():
            print(
                f"ID: {item_id} | Name: {details['name']} | "
                f"Qty: {details['quantity']} | Price: ${details['price']:.2f} | "
                f"Category: {details['category']}"
            )

    def update_item(self, item_id, field, value):
        if item_id not in self.inventory:
            print(f"❌ Item ID '{item_id}' not found.")
            return

        if field not in ("name", "quantity", "price", "category"):
            print("❌ Invalid field. Choose from: name, quantity, price, category.")
            return

        if field == "quantity":
            value = int(value)
        elif field == "price":
            value = float(value)

        self.inventory[item_id][field] = value
        print(f"✅ Item '{item_id}' updated: {field} -> {value}")

    def delete_item(self, item_id):
        if item_id in self.inventory:
            removed = self.inventory.pop(item_id)
            print(f"🗑️  Removed item '{removed['name']}' (ID: {item_id}).")
        else:
            print(f"❌ Item ID '{item_id}' not found.")

    # ---------------------------------------------------------------
    # Reports
    # ---------------------------------------------------------------
    def low_stock_report(self, threshold=LOW_STOCK_THRESHOLD):
        low_items = {
            item_id: details
            for item_id, details in self.inventory.items()
            if details["quantity"] < threshold
        }
        if not low_items:
            print(f"✅ No items below threshold ({threshold}).")
            return

        print(f"⚠️  Items below stock threshold ({threshold}):")
        for item_id, details in low_items.items():
            print(f"  - {details['name']} (ID: {item_id}): {details['quantity']} left")

    def total_inventory_value(self):
        total = sum(
            details["quantity"] * details["price"]
            for details in self.inventory.values()
        )
        print(f"💰 Total inventory value: ${total:.2f}")
        return total

    # ---------------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------------
    def save_to_file(self, filename=DATA_FILE):
        with open(filename, "w") as f:
            json.dump(self.inventory, f, indent=4)
        print(f"💾 Inventory saved to '{filename}'.")

    def load_from_file(self, filename=DATA_FILE):
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found.")
            return
        with open(filename, "r") as f:
            self.inventory = json.load(f)
        print(f"📂 Inventory loaded from '{filename}'.")


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------
def print_menu():
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Add Item")
    print("2. View All Items")
    print("3. Search Item")
    print("4. Update Item")
    print("5. Delete Item")
    print("6. Low Stock Report")
    print("7. Total Inventory Value")
    print("8. Save Inventory")
    print("9. Load Inventory")
    print("0. Exit")
    print("========================================")


def main():
    manager = InventoryManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            item_id = input("Item ID: ").strip()
            name = input("Name: ").strip()
            try:
                quantity = int(input("Quantity: ").strip())
                price = float(input("Price: ").strip())
            except ValueError:
                print("❌ Quantity must be an integer and price must be a number.")
                continue
            category = input("Category: ").strip()
            manager.add_item(item_id, name, quantity, price, category)

        elif choice == "2":
            manager.view_all_items()

        elif choice == "3":
            key = input("Enter item ID or name to search: ").strip()
            manager.search_item(key)

        elif choice == "4":
            item_id = input("Item ID to update: ").strip()
            field = input("Field to update (name/quantity/price/category): ").strip().lower()
            value = input("New value: ").strip()
            try:
                manager.update_item(item_id, field, value)
            except ValueError:
                print("❌ Invalid value for the selected field.")

        elif choice == "5":
            item_id = input("Item ID to delete: ").strip()
            manager.delete_item(item_id)

        elif choice == "6":
            try:
                threshold = input(
                    f"Threshold (default {LOW_STOCK_THRESHOLD}): "
                ).strip()
                threshold = int(threshold) if threshold else LOW_STOCK_THRESHOLD
            except ValueError:
                threshold = LOW_STOCK_THRESHOLD
            manager.low_stock_report(threshold)

        elif choice == "7":
            manager.total_inventory_value()

        elif choice == "8":
            manager.save_to_file()

        elif choice == "9":
            manager.load_from_file()

        elif choice == "0":
            print("👋 Exiting Inventory Management System. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
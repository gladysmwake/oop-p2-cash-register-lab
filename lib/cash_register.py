#!/usr/bin/env python3

class CashRegister:
    """Simulates the core functions of a cash register for an e-commerce site."""

    def __init__(self, discount=0):
        # discount must be an integer between 0 and 100 (inclusive).
        # If it isn't valid, we flag it but still store whatever was passed in
        # so we don't silently hide a bug from the caller.
        if isinstance(discount, int) and 0 <= discount <= 100:
            self.discount = discount
        else:
            print("Not valid discount")
            self.discount = discount

        self.total = 0                     # running total of everything rung up
        self.items = []                    # flat list of item names (repeated per quantity)
        self.previous_transactions = []    # history of add_item calls, used by void_last_transaction

    def add_item(self, item, price, quantity=1):
        """Adds `item` to the register `quantity` times and updates the total."""
        self.total += price * quantity
        self.items.extend([item] * quantity)

        # Keep a record of this exact transaction so it can be undone later.
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity
        })

    def apply_discount(self):
        """Applies the stored discount percentage to the current total."""
        if self.discount:
            self.total -= self.total * self.discount / 100
            # Avoid printing "800.0" when the total is a whole number.
            display_total = int(self.total) if self.total == int(self.total) else round(self.total, 2)
            print(f"After the discount, the total comes to ${display_total}.")
        else:
            print("There is no discount to apply.")

    def void_last_transaction(self):
        """Removes the most recent add_item transaction from the register."""
        if not self.previous_transactions:
            print("There is no previous transaction to void.")
            return

        last_transaction = self.previous_transactions.pop()
        item = last_transaction["item"]
        price = last_transaction["price"]
        quantity = last_transaction["quantity"]

        # Undo the total change from that transaction.
        self.total -= price * quantity

        # Remove that many copies of the item from the end of the items list.
        removed = 0
        for i in range(len(self.items) - 1, -1, -1):
            if removed == quantity:
                break
            if self.items[i] == item:
                del self.items[i]
                removed += 1
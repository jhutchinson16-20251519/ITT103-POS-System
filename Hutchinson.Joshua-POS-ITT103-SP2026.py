# "I CERTIFY THAT I HAVE NOT GIVEN OR RECEIVED ANY UNAUTHORIZED ASSISTANCE ON THIS ASSIGNMENT"
# Electronic Signature: Joshua Hutchinson

TAX = 0.10
DISCOUNT = 0.05
DISCOUNT_MIN = 5000
LOW_STOCK = 5

STORE = "BEST BUY RETAIL STORE"
ADDRESS = "12 Main Street, Kingston, Jamaica"
PHONE = "Tel: (876) 555-0199"

catalog = {
    "Rice (1 kg)":           {"price":  350.00, "stock": 50},
    "Flour (1 kg)":          {"price":  280.00, "stock": 40},
    "Sugar (1 kg)":          {"price":  320.00, "stock": 45},
    "Cooking Oil (1 L)":     {"price":  750.00, "stock": 30},
    "Cornmeal (1 kg)":       {"price":  300.00, "stock": 25},
    "Whole Milk (1 L)":      {"price":  420.00, "stock": 20},
    "Eggs (12 pack)":        {"price":  650.00, "stock": 15},
    "Bread (loaf)":          {"price":  480.00, "stock": 10},
    "Butter (250 g)":        {"price":  560.00, "stock":  8},
    "Canned Tuna (185 g)":   {"price":  380.00, "stock": 35},
    "Dish Soap (500 mL)":    {"price":  320.00, "stock": 22},
    "Toilet Paper (4 rolls)":{"price":  720.00, "stock":  4},
}


def show_menu():
    print("\n" + "=" * 45)
    print(f"         {STORE}")
    print("           CASHIER MENU")
    print("=" * 45)
    print("  [1] View Products")
    print("  [2] Add Item to Cart")
    print("  [3] Remove Item from Cart")
    print("  [4] View Cart")
    print("  [5] Checkout")
    print("  [6] New Transaction")
    print("  [7] Exit")
    print("=" * 45)


def show_catalog():
    print("\n" + "-" * 52)
    print(f"{'#':<4} {'PRODUCT':<24} {'PRICE':>10} {'STOCK':>8}")
    print("-" * 52)
    i = 1
    for name, info in catalog.items():
        note = " LOW!" if info["stock"] < LOW_STOCK else ""
        print(f"{i:<4} {name:<24} {info['price']:>10,.2f} {info['stock']:>6}{note}")
        i += 1
    print("-" * 52)


def show_cart(cart):
    if not cart:
        print("\n  Cart is empty.")
        return
    print("\n" + "-" * 58)
    print(f"  {'ITEM':<24} {'QTY':>4} {'UNIT PRICE':>11} {'TOTAL':>11}")
    print("-" * 58)
    for name, info in cart.items():
        total = info["qty"] * info["price"]
        print(f"  {name:<24} {info['qty']:>4} {info['price']:>11,.2f} {total:>11,.2f}")
    print("-" * 58)


def add_item(cart):
    show_catalog()
    name_input = input("\n  Enter product name (or 0 to cancel): ").strip()
    if name_input == "0":
        return

    found = None
    for key in catalog:
        if key.lower() == name_input.lower():
            found = key
            break

    if found is None:
        print(f"  Product '{name_input}' not found.")
        return

    stock = catalog[found]["stock"]
    if stock == 0:
        print(f"  '{found}' is out of stock.")
        return

    while True:
        qty_input = input(f"  Enter quantity (available: {stock}): ")
        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("  Please enter a valid whole number.")
            continue
        qty = int(qty_input)
        if qty > stock:
            print(f"  Only {stock} available.")
            continue
        break

    price = catalog[found]["price"]

    if found in cart:
        new_qty = cart[found]["qty"] + qty
        if new_qty > stock:
            print(f"  Cannot add that many. Cart already has {cart[found]['qty']}.")
            return
        cart[found]["qty"] = new_qty
    else:
        cart[found] = {"qty": qty, "price": price}

    catalog[found]["stock"] -= qty
    print(f"\n  Added {qty} x {found} to cart.")

    left = catalog[found]["stock"]
    if left < LOW_STOCK:
        print(f"  WARNING: Only {left} unit(s) of '{found}' left in stock!")


def remove_item(cart):
    if not cart:
        print("\n  Cart is empty.")
        return

    show_cart(cart)
    name_input = input("\n  Enter product name to remove (or 0 to cancel): ").strip()
    if name_input == "0":
        return

    found = None
    for key in cart:
        if key.lower() == name_input.lower():
            found = key
            break

    if found is None:
        print(f"  '{name_input}' is not in the cart.")
        return

    current = cart[found]["qty"]
    qty_input = input(f"  How many to remove? (1-{current} or 'all'): ").strip()

    if qty_input.lower() == "all":
        remove_qty = current
    elif qty_input.isdigit() and 0 < int(qty_input) <= current:
        remove_qty = int(qty_input)
    else:
        print("  Invalid quantity.")
        return

    catalog[found]["stock"] += remove_qty
    cart[found]["qty"] -= remove_qty

    if cart[found]["qty"] == 0:
        del cart[found]
        print(f"  '{found}' removed from cart.")
    else:
        print(f"  Removed {remove_qty} unit(s) of '{found}'.")


def get_subtotal(cart):
    total = 0
    for item in cart.values():
        total += item["qty"] * item["price"]
    return total


def get_totals(cart):
    subtotal = get_subtotal(cart)

    discount = 0
    if subtotal > DISCOUNT_MIN:
        discount = subtotal * DISCOUNT

    after_discount = subtotal - discount
    tax = subtotal * TAX
    total_due = after_discount + tax

    return subtotal, discount, tax, total_due


def get_payment(total_due):
    print(f"\n  Total Due: JMD {total_due:,.2f}")
    while True:
        entry = input("  Amount received from customer: JMD ").strip()
        try:
            amount = float(entry)
            if amount < 0:
                print("  Amount cannot be negative.")
            elif amount < total_due:
                print(f"  Not enough. Still needs JMD {total_due - amount:,.2f} more.")
            else:
                return amount
        except ValueError:
            print("  Please enter a valid amount.")


def print_receipt(cart, subtotal, discount, tax, total_due, paid, trans_id):
    import datetime
    change = paid - total_due
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    w = 50

    print("\n" + "=" * w)
    print(STORE.center(w))
    print(ADDRESS.center(w))
    print(PHONE.center(w))
    print("=" * w)
    print(f"  Receipt #: {trans_id:04d}")
    print(f"  Date/Time: {timestamp}")
    print("-" * w)
    print(f"  {'ITEM':<22} {'QTY':>3} {'PRICE':>9} {'TOTAL':>9}")
    print("-" * w)

    for name, info in cart.items():
        line = info["qty"] * info["price"]
        n = (name[:20] + "..") if len(name) > 22 else name
        print(f"  {n:<22} {info['qty']:>3} {info['price']:>9,.2f} {line:>9,.2f}")

    print("-" * w)
    print(f"  {'Subtotal:':<30} {subtotal:>14,.2f}")
    if discount > 0:
        print(f"  {'Discount (5%):':<30} -{discount:>13,.2f}")
    print(f"  {'Tax (10%):':<30} {tax:>14,.2f}")
    print("=" * w)
    print(f"  {'TOTAL DUE:':<30} {total_due:>14,.2f}")
    print(f"  {'Amount Paid:':<30} {paid:>14,.2f}")
    print(f"  {'Change:':<30} {change:>14,.2f}")
    print("=" * w)
    print("      ** THANK YOU FOR SHOPPING WITH US! **")
    print("            Please come again!".center(w))
    print("=" * w + "\n")


def checkout(cart, trans_id):
    if not cart:
        print("\n  Cart is empty. Add items first.")
        return False

    show_cart(cart)
    subtotal, discount, tax, total_due = get_totals(cart)

    print(f"\n  Subtotal  : JMD {subtotal:,.2f}")
    if discount > 0:
        print(f"  Discount  : JMD -{discount:,.2f}  (5% off - bill over ${DISCOUNT_MIN:,})")
    print(f"  Tax (10%) : JMD {tax:,.2f}")
    print(f"  TOTAL DUE : JMD {total_due:,.2f}")

    confirm = input("\n  Proceed to payment? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Checkout cancelled.")
        return False

    paid = get_payment(total_due)
    print_receipt(cart, subtotal, discount, tax, total_due, paid, trans_id)
    return True


def check_low_stock():
    low_items = {k: v for k, v in catalog.items() if v["stock"] < LOW_STOCK}
    if low_items:
        print("\n  LOW STOCK ALERT:")
        for name, info in low_items.items():
            print(f"    - {name}: {info['stock']} remaining")


def main():
    trans_id = 1
    cart = {}

    print("\n" + "=" * 45)
    print(f"  Welcome to {STORE}")
    print("  POS System  |  Spring 2026")
    print("=" * 45)

    while True:
        show_menu()
        choice = input("  Select option [1-7]: ").strip()

        if choice == "1":
            show_catalog()
            check_low_stock()

        elif choice == "2":
            add_item(cart)

        elif choice == "3":
            remove_item(cart)

        elif choice == "4":
            show_cart(cart)
            if cart:
                print(f"  Running Subtotal: JMD {get_subtotal(cart):,.2f}")

        elif choice == "5":
            done = checkout(cart, trans_id)
            if done:
                trans_id += 1
                cart = {}
                print("  Cart cleared. Ready for next customer.")

        elif choice == "6":
            if cart:
                confirm = input("  Cart has items. Start new transaction anyway? (y/n): ").strip().lower()
                if confirm == "y":
                    for name, info in cart.items():
                        catalog[name]["stock"] += info["qty"]
                    cart = {}
                    print("  New transaction started.")
            else:
                cart = {}
                print("  New transaction started.")

        elif choice == "7":
            if cart:
                confirm = input("  Items still in cart. Exit anyway? (y/n): ").strip().lower()
                if confirm != "y":
                    continue
            for name, info in cart.items():
                catalog[name]["stock"] += info["qty"]
            print("\n  Goodbye!\n")
            break

        else:
            print("  Invalid option. Choose 1 to 7.")


main()

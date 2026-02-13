inventory = {
    "Laptop": (999.99, 5),
    "Mouse": (29.99, 15),
    "Keyboard": (79.99, 10),
    "Monitor": (299.99, 8)
}
print("=== Current Inventory ===")
for product, details in inventory.items():
    price = details[0]
    quantity = details[1]
    print(product + " - Price: $" + str(price) + ", Quantity: " + str(quantity))

print()
electronics = {"Laptop", "Monitor"}
accessories = {"Mouse", "Keyboard"}
all_products = electronics | accessories
print("All product categories:", all_products)

prices = []
for product in inventory:
    price = inventory[product][0]
    prices.append(price)
print("Price list:", prices)
prices.sort()
print("Sorted prices:", prices)
print("Lowest price: $" + str(prices[0]))
print("Highest price: $" + str(prices[-1]))

inventory["Headphones"] = (49.99, 20)

mouse_price = inventory["Mouse"][0]
inventory["Mouse"] = (mouse_price, 12)

del inventory["Monitor"]

print("=== Final Inventory ===")
for product, details in inventory.items():
    price = details[0]
    quantity = details[1]
    print(product + " - Price: $" + str(price) + ", Quantity: " + str(quantity))
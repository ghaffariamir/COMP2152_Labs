contacts = {
    "Alice": "555-1234",
    "Bob": "555-5678",
    "Charlie": "555-9999"
}
print("Alice's number:", contacts["Alice"])
contacts["Diana"] = "555-4321"
print("Contacts after adding Diana:", contacts)
contacts["Bob"] = "555-0000"
print("Contacts after updating Bob:", contacts)
del contacts["Charlie"]
print("Contacts after deleting Charlie:", contacts)
print("All names:", contacts.keys())
print("All numbers:", contacts.values())
print("Total contacts:", len(contacts))
monday_class = {"Alice", "Bob", "Charlie", "Diana"}
wednesday_class = {"Bob", "Diana", "Eve", "Frank"}

monday_class.add("Grace")
print("Monday class:", monday_class)
print("Wednesday class:", wednesday_class)
both_classes = monday_class & wednesday_class
print("Attended both classes:", both_classes)
all_students = monday_class | wednesday_class
print("Attended either class:", all_students)
only_monday = monday_class - wednesday_class
print("Only Monday:", only_monday)
only_one = monday_class ^ wednesday_class
print("Only one class (not both):", only_one)
print("Is Monday subset of all students?", monday_class <= all_students)

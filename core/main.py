print("===================================")
print("   LIBRARY MANAGEMENT SYSTEM")
print("===================================")

print("Welcome to Our Library!")

print("1. Add Book")
print("2. View Books")
print("3. Search Book")
print("4. Issue Book")
print("5. Return Book")
print("6. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    print("Add Book Selected")
elif choice == "2":
    print("View Books Selected")
elif choice == "3":
    print("Search Book Selected")
elif choice == "4":
    print("Issue Book Selected")
elif choice == "5":
    print("Return Book Selected")
elif choice == "6":
    print("Thank you!")
else:
    print("Invalid Choice!")
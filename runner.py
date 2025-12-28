from model import task
from logic import Manager


if __name__ == '__main__':
    manager = Manager()

    while True:
        print("\n=== Task Manager ===")
        print("What would you like to do?\n")
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Mark Task as To-Do")
        print("5. View All Completed Tasks")
        print("6. View All To-Do Tasks")
        print("7. Edit Task")
        print("8. Delete Task")
        print("0. Exit\n")

        choice = input("Enter your choice: \n")

        if choice == "1":
            manager.create()

        elif choice == "2":
            manager.read()

        elif choice == "3":
            manager.completed()

        elif choice == "4":
            manager.todo()

        elif choice == "5":
            manager.view_completed()

        elif choice == "6":
            manager.view_todo()

        elif choice == "7":
            manager.edit()

        elif choice == "8":
            manager.delete()

        elif choice == "0":
            print("Thank you for using Task Manager. Goodbye!\n")
            break

        else:
            print("Error: Please enter a valid choice (1-8,0).\n")
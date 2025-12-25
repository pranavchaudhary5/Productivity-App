from model import task
from logic import manager


if __name__ == '__main__':
    Manager = manager()

    while True:
        print("Welcome to the Task App")
        print("What you wanna do today ?\n")
        print("1,  Create Task")
        print("2,  View all Task")
        print("3,  View Specific Task")
        print("4,  Mark Task as Completed")
        print("5,  Mark Task as Todo")
        print("6,  View all Completed Tasks")
        print("7,  View all Todo Tasks")
        print("8,  Edit Task")
        print("9,  Delete Task")
        print("10,  Exit\n")

        choice = input("Enter your choice: \n")

        if choice == "1":
            Manager.create()

        if choice == "2":
            Manager.readall()

        if choice == "3":
            Manager.readone()

        if choice == "4":
            Manager.completed()

        if choice == "5":
            Manager.todo()

        if choice == "6":
            Manager.viewcompleted()

        if choice == "7":
            Manager.viewtodo()

        if choice == "8":
            Manager.edit()

        if choice == "9":
            Manager.delete()

        if choice == "10":
            break



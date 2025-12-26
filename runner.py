from model import task
from logic import manager


if __name__ == '__main__':
    Manager = manager()

    while True:
        print("Welcome to the Task App")
        print("What you wanna do today ?\n")
        print("1,  Create Task")
        print("2,  View Tasks")
        print("3,  Mark Task as Completed")
        print("4,  Mark Task as Todo")
        print("5,  View all Completed Tasks")
        print("6,  View all Todo Tasks")
        print("7,  Edit Task")
        print("8,  Delete Task")
        print("9,  Exit\n")

        choice = input("Enter your choice: \n")

        if choice == "1":
            Manager.create()

        if choice == "2":
            Manager.readall()

        if choice == "3":
            Manager.completed()

        if choice == "4":
            Manager.todo()

        if choice == "5":
            Manager.viewcompleted()

        if choice == "6":
            Manager.viewtodo()

        if choice == "7":
            Manager.edit()

        if choice == "8":
            Manager.delete()

        if choice == "9":
            break



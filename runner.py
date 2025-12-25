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
        print("4,  Edit Task")
        print("5,  Delete Task")
        print("6,  Exit\n")

        choice = input("Enter your choice: \n")
        #CREATE
        if choice == "1":
            Manager.create()

        #READ ALL
        if choice == "2":
            Manager.readall()

        #READ SPECIFIC
        if choice == "3":
            Manager.readone()

        #EDIT
        if choice == "4":
            Manager.edit()

        #DELETE
        if choice == "5":
            Manager.delete()

        #EXIT
        if choice == "6":
            break



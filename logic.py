from model import task

class manager:


    def SearchByID(self):
        userid = int(input("Enter task ID: "))
        for t in self.storage:
            if t.id == userid:
                return t


    def SearchByName(self):
        username = (input("Enter task Name: "))
        for t in self.storage:
            if t.name == username:
                return t


    def __init__(self):
        self.storage = []
        self.i = 0


    def create(self):
        self.i = self.i + 1

        name = input("Enter task name: ")
        content = input("Enter task description: ")

        Task = task()
        Task.set(self.i, name, content)
        self.storage.append(Task)
        print("Task added.\n")


    def readall(self):
        while True:
            text = "S.no:"
            sno = 0
            for t in self.storage:
                sno = sno + 1
                print(text,sno,t)

            print("Enter 1 to View by Serial Number")
            print("Enter 2 to View by Name")
            print("Enter 3 to View by ID")
            print("Enter 4 to Exit")
            print("\n")
            choice1 = int(input("Enter choice: "))

            if choice1 == 1:
                user = int(input("Enter serial number: "))
                print("\n")
                print(self.storage[user-1].name)
                print(self.storage[user-1].id)
                print(self.storage[user-1].status)
                print(self.storage[user-1].content)
                print("\n")

            if choice1 == 2:
                d = self.SearchByName()
                print(d.name)
                print(d.id)
                print(d.status)
                print(d.content)
                print("\n")

            if choice1 == 3:
                d = self.SearchByID()
                print(d.name)
                print(d.id)
                print(d.status)
                print(d.content)
                print("\n")

            if choice1 == 4:
                break


    def completed(self):
        d = self.SearchByID()
        d.status = "Completed"
        print("Task marked as Completed\n")


    def todo(self):
        d = self.SearchByID()
        d.status = "Todo"
        print("Task marked as Todo\n")


    def viewcompleted(self):
        for t in self.storage:
            if t.status == "Completed":
                print(t)


    def viewtodo(self):
        for t in self.storage:
            if t.status == "Todo":
                print(t)


    def edit(self):
        userid = int(input("Enter task ID: "))

        while True:
            print("1,  Edit Task Name")
            print("2,  Edit Task Description")
            print("3,  Exit Editing")

            choice = input("Enter your choice: \n")

            if choice == "1":
                for t in self.storage:
                    if t.id == userid:
                        name = input("Enter new task name: ")
                        t.name = name
                        print("Name Updated")

            if choice == "2":
                for t in self.storage:
                    if t.id == userid:
                        content = input("Enter new task description: ")
                        t.content = content
                        print("Content Updated")

            if choice == "3":
                break


    def delete(self):
        text = "S.no:"
        sno = 0
        for t in self.storage:
            sno = sno + 1
            print(text, sno, t)
        userinput = int(input("Enter serial number to delete: "))
        self.storage.remove(self.storage[userinput-1])
        print("Task deleted")
        print("\n")
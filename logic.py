from model import task


class manager:

    def __init__(self):
        self.storage = []

    def create(self):
        name = input("Enter task name: ")
        content = input("Enter task description: ")

        num = len(self.storage) + 1

        Task = task()
        Task.set(num, name, content)
        self.storage.append(Task)

        print("Task added.\n")

        print("Task ID: ")
        print(self.storage[num - 1].id)

        print("Task Name: ")
        print(self.storage[num - 1].name)

        print("Task Description: ")
        print(self.storage[num - 1].content)
        print("\n")

    def readall(self):
        for t in self.storage:
            print(t)

    def readone(self):
        userid = int(input("Enter task id: "))

        print("Task ID: ")
        print(self.storage[userid - 1].id)

        print("Task Name: ")
        print(self.storage[userid - 1].name)

        print("Task Description: ")
        print(self.storage[userid - 1].content)
        print("\n")

    def edit(self):
        userid = int(input("Enter task id: "))

        while True:
            print("1,  Edit Task Name")
            print("2,  Edit Task Description")
            print("3,  Exit Editing")

            choice = input("Enter your choice: \n")

            if choice == "1":
                name = input("Enter new task name: ")
                self.storage[userid - 1].name = name

            if choice == "2":
                content = input("Enter new task description: ")
                self.storage[userid - 1].content = content

            if choice == "3":
                break

    def delete(self):
        userid = int(input("Enter task id to delete: "))
        self.storage.remove(self.storage[userid - 1])
        print("Task deleted.\n")

        for i in range(1, len(self.storage) + 1):
            self.storage[i - 1].id = i



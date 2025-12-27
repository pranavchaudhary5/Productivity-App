from model import task
class manager:

    def name_check(self,text):
            if len(text) > 50 or len(text) < 1 or not text:
                print("Task name must be between 1 to 50 characters\n")
                return False
            return True

    def content_check(self,text):
            if len(text) > 500 or len(text) < 1 or not text:
                print("Content must be between 1 to 500 characters\n")
                return False
            return True

    def SearchByID(self, u):
        try:
            userid = int(u)
        except ValueError:
            print("Invalid ID")
            return -1

        for tt in self.storage:
            if tt.id == userid:
                return tt
        return None

    def SearchByName(self):
        byname = []
        while True:
            username = (input("Enter task Name: "))
            u = username.strip()
            result = self.name_check(u)
            if not result:
                continue
            break

        i = 0
        for t in self.storage:
            if t.name == u:
                byname.append(t)

        if len(byname) == 0:
            return None

        if len(byname) == 1:
            return byname[0]

        if len(byname) > 1:
            return byname

    def __init__(self):
        self.storage = []
        self.i = 0

    def create(self):

        while True:
            name = input("Enter task name: ")
            n = name.strip()
            result = self.name_check(n)
            if not result:
                continue
            break

        while True:
            content = input("Enter task description: ")
            c = content.strip()
            result = self.content_check(c)
            if not result:
                continue
            break

        self.i = self.i + 1
        Task = task()
        Task.set(self.i, n, c)
        self.storage.append(Task)
        print("Task added.\n")

    def readall(self):
        if not self.storage:
            print("No tasks found.\n")

        else:
            while True:
                text = "S.no:"
                sno = 0
                for t in self.storage:
                    sno = sno + 1
                    print(text, sno, t)

                print("\n")
                print("Enter 1 to View by Serial Number")
                print("Enter 2 to View by Name")
                print("Enter 3 to View by ID")
                print("Enter 4 to Exit\n")

                while True:
                    c1 = (input("Enter choice: "))
                    try:
                        choice1 = int(c1)
                        break
                    except ValueError:
                        print("Invalid Input.\n")

                if choice1 == 1:
                    while True:
                        u = (input("Enter serial number: "))
                        try:
                            user = int(u)

                        except ValueError:
                            print("Invalid Input.\n")
                            continue

                        if len(self.storage) < user:
                            print("Enter Valid Serial Number.\n")
                            continue
                        else:
                            print(self.storage[user - 1].name)
                            print(self.storage[user - 1].id)
                            print(self.storage[user - 1].status)
                            print(self.storage[user - 1].content)
                            print("\n")
                            break

                elif choice1 == 2:
                    d = self.SearchByName()
                    if not d:
                        print("Task Not Found.\n")
                    elif isinstance(d, task):
                        print(d.name)
                        print(d.id)
                        print(d.status)
                        print(d.content)
                        print("\n")

                    elif isinstance(d, list):
                        for t in d:
                            print(t.name, t.id)
                        print("Multiple Task Found, Enter ID to open one")

                        while True:
                            u = (input("Enter task ID: "))
                            result = self.SearchByID(u)
                            if result == -1:
                                continue
                            else:
                                print(result.name)
                                print(result.id)
                                print(result.status)
                                print(result.content)
                                print("\n")
                                break

                elif choice1 == 3:
                    while True:
                        u = (input("Enter task ID: "))
                        d = self.SearchByID(u)
                        if d == -1:
                            continue
                        elif d is None:
                            print("Task Not Found.\n")
                            break
                        else:
                            print(d.name)
                            print(d.id)
                            print(d.status)
                            print(d.content)
                            print("\n")
                            break

                elif choice1 == 4:
                    break

                else:
                    print("Enter valid choice\n")

    def completed(self):
        while True:
            u = (input("Enter task ID: "))
            d = self.SearchByID(u)
            if d == -1:
                continue
            if d is None:
                print("No such task.\n")
                continue
            else:
                if d.status == "Completed":
                    print("Already Marked Completed.\n")
                    break
                else:
                    d.status = "Completed"
                    print("Marked Completed.\n")
                    break

    def todo(self):
        while True:
            u = (input("Enter task ID: "))
            d = self.SearchByID(u)
            if d == -1:
                continue
            if d is None:
                print("No such task.\n")
                continue
            else:
                if d.status == "Todo":
                    print("Already Marked Todo.\n")
                    break
                else:
                    d.status = "Todo"
                    print("Marked Todo\n")
                    break

    def viewcompleted(self):
        if not self.storage:
            print("No tasks found.\n")
        else:
            for t in self.storage:
                if t.status == "Completed":
                    print(t)

    def viewtodo(self):
        if not self.storage:
            print("No tasks found.\n")
        else:
            for t in self.storage:
                if t.status == "Todo":
                    print(t)

    def edit(self):
        while True:
            u = (input("Enter task ID: "))
            d = self.SearchByID(u)
            if d == -1:
                continue
            if d is None:
                print("No such task.\n")
                continue
            else:
                userid = d.id

                while True:
                    print("1,  Edit Task Name")
                    print("2,  Edit Task Description")
                    print("3,  Exit Editing")

                    c = input("Enter your choice: \n")
                    try:
                        choice = int(c)
                    except ValueError:
                        print("Invalid Input.\n")
                        continue

                    if choice == 1:
                        while True:
                            name = input("Enter task New name: ")
                            n = name.strip()
                            result = self.name_check(n)
                            if not result:
                                continue
                            break
                        d.name = n
                        print("Name Updated\n")
                        continue

                    elif choice == 2:
                        while True:
                            content = input("Enter task New description: ")
                            c = content.strip()
                            result = self.content_check(c)
                            if not result:
                                print("Invalid Description")
                                continue
                            break
                        d.content = c
                        print("Content Updated\n")

                    elif choice == 3:
                        break

                    else:
                        print("Enter valid choice\n")
                        print("\n")
            break

    def delete(self):
        if not self.storage:
            print("No tasks found.\n")
        else:
            text = "S.no:"
            sno = 0
            for t in self.storage:
                sno = sno + 1
                print(text, sno, t)

            while True:
                u = (input("Enter ID to delete: "))
                result = self.SearchByID(u)
                if result == -1:
                    continue

                elif not result:
                    print("Incorrect id.\n")
                    continue

                else:
                    iterator = -1
                    for i in self.storage:
                        iterator = iterator + 1
                        if i.id == result.id:
                            break
                    self.storage.remove(self.storage[iterator])
                    print("Task Deleted\n")
                    break


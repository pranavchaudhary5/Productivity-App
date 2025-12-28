from model import task
class Manager:

    def name_check(self,text):
            if len(text) > 50 or len(text) < 1 or not text:
                print("Error: Task name must be between 1 and 50 characters.\n")
                return False
            return True

    def content_check(self,text):
            if len(text) > 500 or len(text) < 1 or not text:
                print("Error: Description must be between 1 and 500 characters.\n")
                return False
            return True

    def search_by_id(self, u):
        for tt in self.storage:
            if tt.id == u:
                return tt
        return None

    def validate_id(self, u):
        try:
            userid = int(u)
            return userid
        except (ValueError, TypeError):
            print("Error: Invalid ID format. Please enter a valid numeric ID.\n")
            return None

    def display_task(self, t):
        print("\n" + "=" * 60)
        print(f"  ID     : {t.id}")
        print(f"  Name   : {t.name}")
        print(f"  Status : [{t.status}]")
        print("-" * 60)
        print("  Description:")
        for line in t.content.split('\n'):
            print(f"    {line}")
        print("=" * 60 + "\n")

    def search_by_name(self):
        byname = []
        while True:
            username = (input("Enter task name: "))
            u = username.strip()
            result = self.name_check(u)
            if not result:
                continue
            break

        for t in self.storage:
            if t.name == u:
                byname.append(t)

        return byname

    def __init__(self):
        self.storage = []
        self.i = 0

    def create(self):

        exit_flag = False
        
        while True:
            name = input("Enter task name (enter 0 to cancel): ")
            if name == "0":
                exit_flag = True
                print("Task creation cancelled.\n")
                break
            n = name.strip()
            result = self.name_check(n)
            if not result:
                continue
            break

        if exit_flag == False:
            while True:
                content = input("Enter task description (enter 0 to cancel): ")
                if content == "0":
                    exit_flag = True
                    print("Task creation cancelled.\n")
                    break
                c = content.strip()
                result = self.content_check(c)
                if not result:
                    continue
                break
        
        if exit_flag == False:
            self.i = self.i + 1
            Task = task()
            Task.set(self.i, n, c)
            self.storage.append(Task)
            print("Task added successfully.\n")

    def read(self):
        if not self.storage:
            print("No tasks found.\n")

        else:
            while True:
                sno = 0
                for t in self.storage:
                    sno = sno + 1
                    print(f"No. {sno}: {t}")

                print("\n")
                print("1. View by Serial Number")
                print("2. View by Name")
                print("3. View by ID")
                print("0. Exit (or press 0 in any input to cancel)\n")

                while True:
                    c1 = (input("Enter choice: "))
                    try:
                        choice1 = int(c1)
                        break
                    except ValueError:
                        print("Error: Please enter a valid choice (1,2,3,0).\n")

                if choice1 == 1:
                    while True:
                        u = (input("Enter serial number (enter 0 to cancel): "))
                        if u == "0":
                            print("Operation cancelled.\n")
                            break
                        try:
                            user = int(u)

                        except ValueError:
                            print("Error: Please enter a valid numeric serial number.\n")
                            continue

                        if len(self.storage) < user:
                            print("Error: Serial number is out of range. Please enter a valid serial number.\n")
                            continue
                        
                        if user < 1:
                            print("Error: Serial number must be at least 1. Please enter a valid serial number.\n")
                            continue
                        
                        else:
                            self.display_task(self.storage[user - 1])
                            break

                elif choice1 == 2:
                    d = self.search_by_name()
                    if not d:
                        print("Error: Task not found.\n")
                    elif isinstance(d, list):
                        if len(d) == 1:
                            self.display_task(d[0])
                        else:
                            for t in d:
                                print(t.name, t.id)
                            print("Multiple tasks found. Please enter the task ID to open one.\n")

                            while True:
                                u = (input("Enter task ID (enter 0 to cancel): "))
                                if u == "0":
                                    print("Operation cancelled.\n")
                                    break
                                userid = self.validate_id(u)
                                if userid is None:
                                    continue
                                result = self.search_by_id(userid)
                                if result is None:
                                    print("Error: Task not found.\n")
                                    continue
                                else:
                                    self.display_task(result)
                                    break
                    else:
                        # single task object
                        self.display_task(d)

                elif choice1 == 3:
                    while True:
                        u = (input("Enter task ID (enter 0 to cancel): "))
                        if u == "0":
                            print("Operation cancelled.\n")
                            break
                        userid = self.validate_id(u)
                        if userid is None:
                            continue
                        d = self.search_by_id(userid)
                        if d is None:
                            print("Error: Task not found.\n")
                            break
                        else:
                            self.display_task(d)
                            break

                elif choice1 == 0:
                    break

                else:
                    print("Error: Please enter a valid choice (1,2,3,0).\n")

    def completed(self):
        exit_flag = False
        
        while True:
            u = (input("Enter task ID (enter 0 to cancel): "))
            if u == "0":
                exit_flag = True
                print("Operation cancelled.\n")
                break
            userid = self.validate_id(u)
            if userid is None:
                continue
            d = self.search_by_id(userid)
            if d is None:
                print("Error: No task found with that ID.\n")
                continue
            else:
                if d.status == "Completed":
                    print("This task is already marked as completed.\n")
                    break
                else:
                    d.status = "Completed"
                    print("Task marked as completed.\n")
                    break

    def todo(self):
        exit_flag = False
        
        while True:
            u = (input("Enter task ID (enter 0 to cancel): "))
            if u == "0":
                exit_flag = True
                print("Operation cancelled.\n")
                break
            userid = self.validate_id(u)
            if userid is None:
                continue
            d = self.search_by_id(userid)
            if d is None:
                print("Error: No task found with that ID.\n")
                continue
            else:
                if d.status == "Todo":
                    print("This task is already marked as To-Do.\n")
                    break
                else:
                    d.status = "Todo"
                    print("Task marked as To-Do.\n")
                    break

    def view_completed(self):
        if not self.storage:
            print("No tasks found.\n")
        else:
            for t in self.storage:
                if t.status == "Completed":
                    print(t)
                    found = True
                if not found:
                    print("No completed tasks found.\n")

    def view_todo(self):
        if not self.storage:
            print("No tasks found.\n")
        else:
            for t in self.storage:
                if t.status == "Todo":
                    print(t)
                    found = True
                if not found:
                    print("No To-Do tasks found.\n")

    def edit(self):
        exit_flag = False
        
        while True:
            u = (input("Enter task ID (enter 0 to cancel): "))
            if u == "0":
                exit_flag = True
                print("Operation cancelled.\n")
                break
            userid = self.validate_id(u)
            if userid is None:
                continue
            d = self.search_by_id(userid)
            if d is None:
                print("Error: No task found with that ID.\n")
                continue
            else:
                userid = d.id

                while True:
                    print("1. Edit Task Name")
                    print("2. Edit Task Description")
                    print("0. Exit Editing")

                    c = input("Enter your choice: \n")
                    try:
                        choice = int(c)
                    except ValueError:
                        print("Error: Please enter a valid choice (1,2,0).\n")
                        continue

                    if choice == 1:
                        while True:
                            name = input("Enter new task name (enter 0 to cancel): ")
                            if name == "0":
                                print("Edit cancelled.\n")
                                break
                            n = name.strip()
                            result = self.name_check(n)
                            if not result:
                                continue
                            break
                        if name != "0":
                            d.name = n
                            print("Task name updated successfully.\n")
                        continue

                    elif choice == 2:
                        while True:
                            content = input("Enter new task description (enter 0 to cancel): ")
                            if content == "0":
                                print("Edit cancelled.\n")
                                break
                            c = content.strip()
                            result = self.content_check(c)
                            if not result:
                                continue
                            break
                        if content != "0":
                            d.content = c
                            print("Task description updated successfully.\n")

                    elif choice == 0:
                        print("Exiting edit menu.\n")
                        break

                    else:
                        print("Error: Please enter a valid choice (1,2,0).\n")
            break

    def delete(self):
        if not self.storage:
            print("No tasks found.\n")
        else:
            exit_flag = False
            
            sno = 0
            for t in self.storage:
                sno = sno + 1
                print(f"No. {sno}: {t}")

            while True:
                u = (input("Enter ID to delete (enter 0 to cancel): "))
                if u == "0":
                    exit_flag = True
                    print("Operation cancelled.\n")
                    break
                
                userid = self.validate_id(u)
                if userid is None:
                    continue

                result = self.search_by_id(userid)
                if not result:
                    print("Error: Invalid ID. No task found with that ID.\n")
                    continue
                else:
                    self.storage.remove(result)
                    print("Task deleted successfully.\n")
                    break


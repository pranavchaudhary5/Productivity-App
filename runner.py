"""
Task Manager CLI User Interface

This module handles all user interaction (input/output) for the task management system.

Architecture:
- Pure UI logic - no business logic
- All business operations delegated to Manager class
- All responses handled as Pydantic models from Manager

Helper functions:
- get_task_id_from_user(): Get and validate task ID input
- get_task_name_from_user(): Get and validate task name input
- get_task_content_from_user(): Get and validate task content input

Menu functions (each handles one main menu operation):
- create_task()
- view_tasks()
- mark_task_completed()
- mark_task_todo()
- view_completed_tasks()
- view_todo_tasks()
- edit_task()
- delete_task()
"""

from model import task, TaskSchema
from logic import Manager
from validators import validate_id
from formatters import display_task


def display_task_detail(task_schema: TaskSchema):
    """
    Display detailed task information.
    
    Args:
        task_schema (TaskSchema): Task data to display
    """
    print(f"ID: {task_schema.id}")
    print(f"Name: {task_schema.name}")
    print(f"Description: {task_schema.content}")
    print(f"Status: {task_schema.status}\n")


def get_task_id_from_user(prompt="Enter task ID (enter 0 to cancel): "):
    """
    Get and validate task ID from user input.
    
    Loops until valid ID or user enters 0 to cancel.
    
    Args:
        prompt (str): Prompt message for user
        
    Returns:
        Optional[int]: Parsed task ID or None if user cancelled
    """
    while True:
        u = input(prompt)
        if u == "0":
            return None
        validation = validate_id(u)
        if not validation.success:
            print(f"Error: {validation.message}\n")
            continue
        return validation.data


def get_task_name_from_user(prompt="Enter task name (enter 0 to cancel): "):
    """
    Get task name from user input.
    
    Args:
        prompt (str): Prompt message for user
        
    Returns:
        Optional[str]: Task name or None if user entered 0
    """
    while True:
        name = input(prompt)
        if name == "0":
            return None
        return name.strip()


def get_task_content_from_user(prompt="Enter task description (enter 0 to cancel): "):
    """
    Get task content from user input.
    
    Args:
        prompt (str): Prompt message for user
        
    Returns:
        Optional[str]: Task content or None if user entered 0
    """
    while True:
        content = input(prompt)
        if content == "0":
            return None
        return content.strip()


def create_task(manager):
    """
    UI flow for creating a new task.
    
    Gets name and content from user, validates them,
    and calls manager.add_task().
    
    Args:
        manager (Manager): Manager instance
    """
    name = get_task_name_from_user("Enter task name (enter 0 to cancel): ")
    if name is None:
        print("Task creation cancelled.\n")
        return
    
    content = get_task_content_from_user("Enter task description (enter 0 to cancel): ")
    if content is None:
        print("Task creation cancelled.\n")
        return
    
    response = manager.add_task(name, content)
    print(f"{response.message}\n")


def view_tasks(manager):
    """
    UI flow for viewing tasks with multiple search options.
    
    Menu options:
    1. View by serial number (position in list)
    2. View by name (search and filter)
    3. View by ID (exact ID match)
    
    Args:
        manager (Manager): Manager instance
    """
    response = manager.get_all_tasks()
    tasks = response.data
    
    if not tasks:
        print("No tasks found.\n")
        return
    
    while True:
        # Display all tasks
        for sno, t in enumerate(tasks, 1):
            print(f"No. {sno}: {t.name} [{t.id}]")
        
        print("\n1. View by Serial Number")
        print("2. View by Name")
        print("3. View by ID")
        print("0. Exit\n")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            while True:
                user_input = input("Enter serial number (enter 0 to cancel): ")
                if user_input == "0":
                    print("Operation cancelled.\n")
                    break
                try:
                    serial = int(user_input)
                    if serial < 1 or serial > len(tasks):
                        print("Error: Serial number is out of range.\n")
                        continue
                    task_obj = tasks[serial - 1]
                    display_task_detail(task_obj)
                    break
                except ValueError:
                    print("Error: Please enter a valid numeric serial number.\n")
        
        elif choice == "2":
            name = get_task_name_from_user("Enter task name: ")
            if name:
                found_tasks = manager.search_by_name(name)
                if not found_tasks:
                    print("Error: Task not found.\n")
                elif len(found_tasks) == 1:
                    display_task_detail(TaskSchema(id=found_tasks[0].id, name=found_tasks[0].name, content=found_tasks[0].content, status=found_tasks[0].status))
                else:
                    for t in found_tasks:
                        print(f"{t.name} [ID: {t.id}]")
                    task_id = get_task_id_from_user("Enter task ID to view: ")
                    if task_id:
                        task_obj = manager.search_by_id(task_id)
                        if task_obj:
                            display_task_detail(TaskSchema(id=task_obj.id, name=task_obj.name, content=task_obj.content, status=task_obj.status))
                        else:
                            print("Error: Task not found.\n")
        
        elif choice == "3":
            task_id = get_task_id_from_user("Enter task ID: ")
            if task_id:
                task_obj = manager.search_by_id(task_id)
                if task_obj:
                    display_task_detail(TaskSchema(id=task_obj.id, name=task_obj.name, content=task_obj.content, status=task_obj.status))
                else:
                    print("Error: Task not found.\n")
        
        elif choice == "0":
            break
        
        else:
            print("Error: Please enter a valid choice (1,2,3,0).\n")


def mark_task_completed(manager):
    """
    UI flow for marking a task as completed.
    
    Gets task ID from user and calls manager.mark_completed().
    
    Args:
        manager (Manager): Manager instance
    """
    task_id = get_task_id_from_user()
    if task_id:
        response = manager.mark_completed(task_id)
        print(f"{response.message}\n")


def mark_task_todo(manager):
    """
    UI flow for marking a task as to-do.
    
    Gets task ID from user and calls manager.mark_todo().
    
    Args:
        manager (Manager): Manager instance
    """
    task_id = get_task_id_from_user()
    if task_id:
        response = manager.mark_todo(task_id)
        print(f"{response.message}\n")


def view_completed_tasks(manager):
    """
    UI flow for viewing all completed tasks.
    
    Calls manager.get_completed_tasks() and displays results.
    
    Args:
        manager (Manager): Manager instance
    """
    response = manager.get_completed_tasks()
    if not response.data:
        print(f"{response.message}\n")
    else:
        for t in response.data:
            print(f"{t.name} [{t.id}]")
        print()


def view_todo_tasks(manager):
    """
    UI flow for viewing all to-do tasks.
    
    Calls manager.get_todo_tasks() and displays results.
    
    Args:
        manager (Manager): Manager instance
    """
    response = manager.get_todo_tasks()
    if not response.data:
        print(f"{response.message}\n")
    else:
        for t in response.data:
            print(f"{t.name} [{t.id}]")
        print()


def edit_task(manager):
    """
    UI flow for editing a task.
    
    Menu options:
    1. Edit task name
    2. Edit task description
    
    Gets task ID and field to edit, validates, and calls manager.update_task().
    
    Args:
        manager (Manager): Manager instance
    """
    task_id = get_task_id_from_user("Enter task ID (enter 0 to cancel): ")
    if task_id is None:
        print("Operation cancelled.\n")
        return
    
    task_obj = manager.search_by_id(task_id)
    if task_obj is None:
        print("Error: No task found with that ID.\n")
        return
    
    while True:
        print("1. Edit Task Name")
        print("2. Edit Task Description")
        print("0. Exit Editing\n")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            new_name = get_task_name_from_user("Enter new task name (enter 0 to cancel): ")
            if new_name:
                response = manager.update_task(task_id, new_name=new_name)
                print(f"{response.message}\n")
        
        elif choice == "2":
            new_content = get_task_content_from_user("Enter new task description (enter 0 to cancel): ")
            if new_content:
                response = manager.update_task(task_id, new_content=new_content)
                print(f"{response.message}\n")
        
        elif choice == "0":
            print("Exiting edit menu.\n")
            break
        
        else:
            print("Error: Please enter a valid choice (1,2,0).\n")


def delete_task(manager):
    """
    UI flow for deleting a task.
    
    Lists all tasks and gets task ID to delete.
    Calls manager.delete_task().
    
    Args:
        manager (Manager): Manager instance
    """
    response = manager.get_all_tasks()
    tasks = response.data
    
    if not tasks:
        print("No tasks found.\n")
        return
    
    for sno, t in enumerate(tasks, 1):
        print(f"No. {sno}: {t.name} [{t.id}]")
    print()
    
    task_id = get_task_id_from_user("Enter task ID to delete (enter 0 to cancel): ")
    if task_id:
        response = manager.delete_task(task_id)
        print(f"{response.message}\n")


if __name__ == '__main__':
    """Main entry point - CLI menu loop."""
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

        choice = input("Enter your choice: ")

        if choice == "1":
            create_task(manager)

        elif choice == "2":
            view_tasks(manager)

        elif choice == "3":
            mark_task_completed(manager)

        elif choice == "4":
            mark_task_todo(manager)

        elif choice == "5":
            view_completed_tasks(manager)

        elif choice == "6":
            view_todo_tasks(manager)

        elif choice == "7":
            edit_task(manager)

        elif choice == "8":
            delete_task(manager)

        elif choice == "0":
            print("Thank you for using Task Manager. Goodbye!\n")
            break

        else:
            print("Error: Please enter a valid choice (1-8, 0).\n")


def create_task(manager):
    """UI for creating a new task"""
    name = get_task_name_from_user("Enter task name (enter 0 to cancel): ")
    if name is None:
        print("Task creation cancelled.\n")
        return
    
    content = get_task_content_from_user("Enter task description (enter 0 to cancel): ")
    if content is None:
        print("Task creation cancelled.\n")
        return
    
    response = manager.add_task(name, content)
    print(f"{response.message}\n")


def view_tasks(manager):
    """UI for viewing tasks"""
    response = manager.get_all_tasks()
    tasks = response.data
    
    if not tasks:
        print("No tasks found.\n")
        return
    
    while True:
        # Display all tasks
        for sno, t in enumerate(tasks, 1):
            print(f"No. {sno}: {t.name} [{t.id}]")
        
        print("\n1. View by Serial Number")
        print("2. View by Name")
        print("3. View by ID")
        print("0. Exit\n")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            while True:
                user_input = input("Enter serial number (enter 0 to cancel): ")
                if user_input == "0":
                    print("Operation cancelled.\n")
                    break
                try:
                    serial = int(user_input)
                    if serial < 1 or serial > len(tasks):
                        print("Error: Serial number is out of range.\n")
                        continue
                    task_obj = tasks[serial - 1]
                    display_task_detail(task_obj)
                    break
                except ValueError:
                    print("Error: Please enter a valid numeric serial number.\n")
        
        elif choice == "2":
            name = get_task_name_from_user("Enter task name: ")
            if name:
                found_tasks = manager.search_by_name(name)
                if not found_tasks:
                    print("Error: Task not found.\n")
                elif len(found_tasks) == 1:
                    display_task_detail(TaskSchema(id=found_tasks[0].id, name=found_tasks[0].name, content=found_tasks[0].content, status=found_tasks[0].status))
                else:
                    for t in found_tasks:
                        print(f"{t.name} [ID: {t.id}]")
                    task_id = get_task_id_from_user("Enter task ID to view: ")
                    if task_id:
                        task_obj = manager.search_by_id(task_id)
                        if task_obj:
                            display_task_detail(TaskSchema(id=task_obj.id, name=task_obj.name, content=task_obj.content, status=task_obj.status))
                        else:
                            print("Error: Task not found.\n")
        
        elif choice == "3":
            task_id = get_task_id_from_user("Enter task ID: ")
            if task_id:
                task_obj = manager.search_by_id(task_id)
                if task_obj:
                    display_task_detail(TaskSchema(id=task_obj.id, name=task_obj.name, content=task_obj.content, status=task_obj.status))
                else:
                    print("Error: Task not found.\n")
        
        elif choice == "0":
            break
        
        else:
            print("Error: Please enter a valid choice (1,2,3,0).\n")


def mark_task_completed(manager):
    """UI for marking task as completed"""
    task_id = get_task_id_from_user()
    if task_id:
        response = manager.mark_completed(task_id)
        print(f"{response.message}\n")


def mark_task_todo(manager):
    """UI for marking task as to-do"""
    task_id = get_task_id_from_user()
    if task_id:
        response = manager.mark_todo(task_id)
        print(f"{response.message}\n")


def view_completed_tasks(manager):
    """UI for viewing all completed tasks"""
    response = manager.get_completed_tasks()
    if not response.data:
        print(f"{response.message}\n")
    else:
        for t in response.data:
            print(f"{t.name} [{t.id}]")
        print()


def view_todo_tasks(manager):
    """UI for viewing all to-do tasks"""
    response = manager.get_todo_tasks()
    if not response.data:
        print(f"{response.message}\n")
    else:
        for t in response.data:
            print(f"{t.name} [{t.id}]")
        print()


def edit_task(manager):
    """UI for editing a task"""
    task_id = get_task_id_from_user("Enter task ID (enter 0 to cancel): ")
    if task_id is None:
        print("Operation cancelled.\n")
        return
    
    task_obj = manager.search_by_id(task_id)
    if task_obj is None:
        print("Error: No task found with that ID.\n")
        return
    
    while True:
        print("1. Edit Task Name")
        print("2. Edit Task Description")
        print("0. Exit Editing\n")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            new_name = get_task_name_from_user("Enter new task name (enter 0 to cancel): ")
            if new_name:
                response = manager.update_task(task_id, new_name=new_name)
                print(f"{response.message}\n")
        
        elif choice == "2":
            new_content = get_task_content_from_user("Enter new task description (enter 0 to cancel): ")
            if new_content:
                response = manager.update_task(task_id, new_content=new_content)
                print(f"{response.message}\n")
        
        elif choice == "0":
            print("Exiting edit menu.\n")
            break
        
        else:
            print("Error: Please enter a valid choice (1,2,0).\n")


def delete_task(manager):
    """UI for deleting a task"""
    response = manager.get_all_tasks()
    tasks = response.data
    
    if not tasks:
        print("No tasks found.\n")
        return
    
    for sno, t in enumerate(tasks, 1):
        print(f"No. {sno}: {t.name} [{t.id}]")
    print()
    
    task_id = get_task_id_from_user("Enter task ID to delete (enter 0 to cancel): ")
    if task_id:
        response = manager.delete_task(task_id)
        print(f"{response.message}\n")


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

        choice = input("Enter your choice: ")

        if choice == "1":
            create_task(manager)

        elif choice == "2":
            view_tasks(manager)

        elif choice == "3":
            mark_task_completed(manager)

        elif choice == "4":
            mark_task_todo(manager)

        elif choice == "5":
            view_completed_tasks(manager)

        elif choice == "6":
            view_todo_tasks(manager)

        elif choice == "7":
            edit_task(manager)

        elif choice == "8":
            delete_task(manager)

        elif choice == "0":
            print("Thank you for using Task Manager. Goodbye!\n")
            break

        else:
            print("Error: Please enter a valid choice (1-8, 0).\n")

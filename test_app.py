"""
Automated test suite for Task Manager application.

Tests all major functionality:
- Task creation
- Task viewing (all, by ID, by name)
- Task status updates (mark completed/todo)
- Task editing
- Task deletion
- Input validation
"""

from logic import Manager
from validators import name_check, content_check, validate_id


def test_validators():
    """Test validation functions."""
    print("=" * 60)
    print("TESTING VALIDATORS")
    print("=" * 60)
    
    # Test name_check
    print("\n1. Testing name_check():")
    valid_name = name_check("Valid Task Name")
    print(f"   Valid name: {valid_name.success} - {valid_name.message}")
    
    invalid_name = name_check("")
    print(f"   Empty name: {invalid_name.success} - {invalid_name.message}")
    
    long_name = name_check("x" * 51)
    print(f"   Too long name: {long_name.success} - {long_name.message}")
    
    # Test content_check
    print("\n2. Testing content_check():")
    valid_content = content_check("Valid task content")
    print(f"   Valid content: {valid_content.success} - {valid_content.message}")
    
    invalid_content = content_check("")
    print(f"   Empty content: {invalid_content.success} - {invalid_content.message}")
    
    long_content = content_check("x" * 501)
    print(f"   Too long content: {long_content.success} - {long_content.message}")
    
    # Test validate_id
    print("\n3. Testing validate_id():")
    valid_id = validate_id("5")
    print(f"   Valid ID '5': {valid_id.success} - data={valid_id.data}")
    
    invalid_id = validate_id("abc")
    print(f"   Invalid ID 'abc': {invalid_id.success} - {invalid_id.message}")


def test_manager():
    """Test Manager class CRUD operations."""
    print("\n" + "=" * 60)
    print("TESTING MANAGER CLASS")
    print("=" * 60)
    
    manager = Manager()
    
    # Test 1: Add tasks
    print("\n1. Creating Tasks:")
    task1 = manager.add_task("Buy groceries", "Need to buy milk, bread, and eggs")
    print(f"   Task 1: {task1.success} - {task1.message}")
    print(f"   Created task ID: {task1.data.id if task1.data else 'N/A'}")
    
    task2 = manager.add_task("Complete project", "Finish the Python refactoring project")
    print(f"   Task 2: {task2.success} - {task2.message}")
    print(f"   Created task ID: {task2.data.id if task2.data else 'N/A'}")
    
    task3 = manager.add_task("Exercise", "30 minutes workout")
    print(f"   Task 3: {task3.success} - {task3.message}")
    print(f"   Created task ID: {task3.data.id if task3.data else 'N/A'}")
    
    # Test invalid task creation
    invalid_task = manager.add_task("", "Empty name")
    print(f"   Invalid task (empty name): {invalid_task.success} - {invalid_task.message}")
    
    # Test 2: Get all tasks
    print("\n2. Getting All Tasks:")
    all_tasks = manager.get_all_tasks()
    print(f"   {all_tasks.message}")
    print(f"   Total tasks: {len(all_tasks.data)}")
    for t in all_tasks.data:
        print(f"   - [{t.id}] {t.name} (Status: {t.status})")
    
    # Test 3: Search by ID
    print("\n3. Searching Tasks:")
    search_id = manager.search_by_id(1)
    print(f"   Search by ID (1): {search_id.name if search_id else 'Not found'}")
    
    search_name = manager.search_by_name("Exercise")
    print(f"   Search by name ('Exercise'): Found {len(search_name)} task(s)")
    
    # Test 4: Mark task as completed
    print("\n4. Marking Task as Completed:")
    mark_completed = manager.mark_completed(1)
    print(f"   {mark_completed.message}")
    print(f"   Task status: {mark_completed.data.status if mark_completed.data else 'N/A'}")
    
    # Try marking already completed task
    already_completed = manager.mark_completed(1)
    print(f"   Try marking again: {already_completed.success} - {already_completed.message}")
    
    # Test 5: Mark task as todo
    print("\n5. Marking Task as To-Do:")
    mark_todo = manager.mark_todo(1)
    print(f"   {mark_todo.message}")
    print(f"   Task status: {mark_todo.data.status if mark_todo.data else 'N/A'}")
    
    # Test 6: Get completed tasks
    print("\n6. Getting Completed Tasks:")
    manager.mark_completed(2)
    completed = manager.get_completed_tasks()
    print(f"   {completed.message}")
    print(f"   Total completed: {len(completed.data)}")
    for t in completed.data:
        print(f"   - [{t.id}] {t.name}")
    
    # Test 7: Get todo tasks
    print("\n7. Getting To-Do Tasks:")
    todo = manager.get_todo_tasks()
    print(f"   {todo.message}")
    print(f"   Total to-do: {len(todo.data)}")
    for t in todo.data:
        print(f"   - [{t.id}] {t.name}")
    
    # Test 8: Update task
    print("\n8. Updating Task:")
    update = manager.update_task(3, new_name="Gym session", new_content="1 hour workout")
    print(f"   {update.message}")
    print(f"   Updated task: {update.data.name if update.data else 'N/A'}")
    
    # Test invalid update
    invalid_update = manager.update_task(999, new_name="Test")
    print(f"   Update non-existent task: {invalid_update.success} - {invalid_update.message}")
    
    # Test 9: Delete task
    print("\n9. Deleting Task:")
    delete = manager.delete_task(2)
    print(f"   {delete.message}")
    
    remaining = manager.get_all_tasks()
    print(f"   Remaining tasks: {len(remaining.data)}")
    
    # Test invalid delete
    invalid_delete = manager.delete_task(999)
    print(f"   Delete non-existent task: {invalid_delete.success} - {invalid_delete.message}")


def test_pydantic_models():
    """Test Pydantic model serialization."""
    print("\n" + "=" * 60)
    print("TESTING PYDANTIC MODELS")
    print("=" * 60)
    
    manager = Manager()
    task = manager.add_task("Test JSON", "Testing Pydantic serialization")
    
    print("\n1. OperationResponse JSON:")
    print(f"   {task.model_dump_json(indent=2)}")
    
    print("\n2. TaskListResponse JSON:")
    all_tasks = manager.get_all_tasks()
    print(f"   {all_tasks.model_dump_json(indent=2)}")


if __name__ == "__main__":
    test_validators()
    test_manager()
    test_pydantic_models()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)

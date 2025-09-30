from core import tasks, storage
from datetime import datetime, timedelta
import json
import os

def show_tasks(task_list, filter_type="all", search_term=""):
    filtered_tasks = tasks.filter_tasks(task_list, filter_type, search_term)
    
    if not filtered_tasks:
        print("\n✅ No tasks found!\n")
        return
    
    print(f"\n📌 Your To-Do List ({filter_type} tasks):")
    for i, task in enumerate(filtered_tasks, start=1):
        status = "✔" if task["done"] else "❌"
        priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        priority_icon = priority_icons.get(task.get("priority", "medium"), "⚪")
        
        due_info = ""
        if task.get("due_date"):
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
            days_left = (due_date - datetime.now()).days
            if days_left < 0:
                due_info = f" [OVERDUE: {-days_left}d]"
            elif days_left == 0:
                due_info = " [Due: TODAY]"
            else:
                due_info = f" [Due: {days_left}d]"
        
        category_info = f" [{task['category']}]" if task.get("category") else ""
        tags_info = f" {''.join(['#' + tag for tag in task.get('tags', [])])}" if task.get('tags') else ""
        
        print(f"{i}. {task['title']} {priority_icon}{due_info}{category_info}{tags_info} [{status}]")
        
        if task.get('description'):
            print(f"   📝 {task['description']}")

def show_statistics(task_list):
    total_tasks = len(task_list)
    completed_tasks = len([t for t in task_list if t["done"]])
    pending_tasks = total_tasks - completed_tasks
    
    high_priority = len([t for t in task_list if t.get("priority") == "high" and not t["done"]])
    overdue_tasks = len([t for t in task_list if t.get("due_date") and 
                        datetime.strptime(t["due_date"], "%Y-%m-%d") < datetime.now() and not t["done"]])
    
    print("\n📊 Task Statistics:")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed: {completed_tasks} ({completed_tasks/total_tasks*100:.1f}%)" if total_tasks > 0 else "Completed: 0")
    print(f"Pending: {pending_tasks}")
    print(f"High priority pending: {high_priority}")
    print(f"Overdue: {overdue_tasks}")

def input_priority():
    while True:
        priority = input("Priority (high/medium/low) [medium]: ").lower().strip()
        if not priority:
            return "medium"
        if priority in ["high", "medium", "low"]:
            return priority
        print("❌ Invalid priority! Choose from: high, medium, low")

def input_due_date():
    while True:
        due_date = input("Due date (YYYY-MM-DD) or +days [optional]: ").strip()
        if not due_date:
            return None
        if due_date.startswith('+'):
            try:
                days = int(due_date[1:])
                due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                return due_date
            except ValueError:
                print("❌ Invalid format! Use +number (e.g., +7 for 7 days from now)")
        else:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                return due_date
            except ValueError:
                print("❌ Invalid date format! Use YYYY-MM-DD")

def input_tags():
    tags_input = input("Tags (comma-separated) [optional]: ").strip()
    if tags_input:
        return [tag.strip() for tag in tags_input.split(",")]
    return []

def export_tasks(task_list, filename="tasks_export.json"):
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_tasks": len(task_list),
        "tasks": task_list
    }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    print(f"✅ Tasks exported to {filename}")

def import_tasks():
    filename = input("Enter filename to import from: ").strip()
    if not os.path.exists(filename):
        print("❌ File not found!")
        return []
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):  # Old format
            return data
        elif isinstance(data, dict) and "tasks" in data:  # New format
            return data["tasks"]
        else:
            print("❌ Invalid file format!")
            return []
    except Exception as e:
        print(f"❌ Error importing tasks: {e}")
        return []

def show_categories(task_list):
    categories = set(task.get("category", "Uncategorized") for task in task_list)
    print("\n📂 Categories:")
    for i, category in enumerate(sorted(categories), 1):
        count = len([t for t in task_list if t.get("category", "Uncategorized") == category])
        print(f"{i}. {category} ({count} tasks)")

def run_cli():
    task_list = storage.load_tasks()
    history = []  # For undo functionality

    while True:
        print("\n" + "="*50)
        print("🎯 ADVANCED CLI TO-DO MANAGER")
        print("="*50)
        print("1. 📋 View tasks (with filters)")
        print("2. ➕ Add task")
        print("3. ✔️ Mark task as done/undone")
        print("4. 🗑️ Delete task")
        print("5. ✏️ Edit task")
        print("6. 🔍 Search tasks")
        print("7. 📊 Show statistics")
        print("8. 📂 Manage categories")
        print("9. 💾 Export tasks")
        print("10. 📥 Import tasks")
        print("11. ↩️ Undo last action")
        print("12. 🚪 Exit")

        choice = input("\nChoose option (1-12): ").strip()

        if choice == "1":
            print("\n🔍 View Options:")
            print("a. All tasks")
            print("b. Pending tasks")
            print("c. Completed tasks")
            print("d. High priority tasks")
            print("e. Overdue tasks")
            view_choice = input("Choose view option: ").lower()
            
            filters = {"a": "all", "b": "pending", "c": "completed", "d": "high", "e": "overdue"}
            filter_type = filters.get(view_choice, "all")
            
            search_term = ""
            if view_choice == "a":  # Only search in all tasks view
                search_term = input("Search term [optional]: ").strip()
            
            show_tasks(task_list, filter_type, search_term)

        elif choice == "2":
            # Save state for undo
            history.append(task_list.copy())
            if len(history) > 10:  # Keep only last 10 actions
                history.pop(0)
                
            title = input("Enter task title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                continue
                
            description = input("Description [optional]: ").strip()
            category = input("Category [optional]: ").strip()
            priority = input_priority()
            due_date = input_due_date()
            tags = input_tags()

            task_list = tasks.add_task(task_list, title, description, category, priority, due_date, tags)
            storage.save_tasks(task_list)
            print("✅ Task added successfully!")

        elif choice == "3":
            show_tasks(task_list)
            try:
                num = int(input("Enter task number to toggle: ")) - 1
                if 0 <= num < len(task_list):
                    # Save state for undo
                    history.append(task_list.copy())
                    if len(history) > 10:
                        history.pop(0)
                        
                    task_list = tasks.toggle_task(task_list, num)
                    storage.save_tasks(task_list)
                    status = "done" if task_list[num]["done"] else "pending"
                    print(f"✅ Task marked as {status}!")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == "4":
            show_tasks(task_list)
            try:
                num = int(input("Enter task number to delete: ")) - 1
                if 0 <= num < len(task_list):
                    # Save state for undo
                    history.append(task_list.copy())
                    if len(history) > 10:
                        history.pop(0)
                        
                    task_list = tasks.delete_task(task_list, num)
                    storage.save_tasks(task_list)
                    print("🗑️ Task deleted!")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == "5":
            show_tasks(task_list)
            try:
                num = int(input("Enter task number to edit: ")) - 1
                if 0 <= num < len(task_list):
                    # Save state for undo
                    history.append(task_list.copy())
                    if len(history) > 10:
                        history.pop(0)
                        
                    task = task_list[num]
                    print(f"Editing: {task['title']}")
                    
                    new_title = input(f"New title [{task['title']}]: ").strip()
                    if new_title:
                        task['title'] = new_title
                    
                    new_desc = input(f"New description [{task.get('description', '')}]: ").strip()
                    task['description'] = new_desc if new_desc else task.get('description', '')
                    
                    new_category = input(f"New category [{task.get('category', '')}]: ").strip()
                    task['category'] = new_category if new_category else task.get('category', '')
                    
                    print(f"Current priority: {task.get('priority', 'medium')}")
                    task['priority'] = input_priority()
                    
                    print(f"Current due date: {task.get('due_date', 'None')}")
                    task['due_date'] = input_due_date()
                    
                    print(f"Current tags: {', '.join(task.get('tags', []))}")
                    task['tags'] = input_tags()
                    
                    storage.save_tasks(task_list)
                    print("✅ Task updated!")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == "6":
            search_term = input("Enter search term: ").strip()
            show_tasks(task_list, "all", search_term)

        elif choice == "7":
            show_statistics(task_list)

        elif choice == "8":
            show_categories(task_list)

        elif choice == "9":
            filename = input("Export filename [tasks_export.json]: ").strip()
            if not filename:
                filename = "tasks_export.json"
            export_tasks(task_list, filename)

        elif choice == "10":
            # Save state for undo
            history.append(task_list.copy())
            if len(history) > 10:
                history.pop(0)
                
            imported_tasks = import_tasks()
            if imported_tasks:
                task_list.extend(imported_tasks)
                storage.save_tasks(task_list)
                print(f"✅ Imported {len(imported_tasks)} tasks!")

        elif choice == "11":
            if history:
                task_list = history.pop()
                storage.save_tasks(task_list)
                print("✅ Last action undone!")
            else:
                print("❌ No actions to undo!")

        elif choice == "12":
            print("👋 Goodbye! Keep being productive! 🚀")
            break

        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    run_cli()
import json
import os
from datetime import datetime

# Create data directory if it doesn't exist
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "todo.json")

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_tasks():
    """Load tasks from JSON file with error handling"""
    ensure_data_dir()
    
    if not os.path.exists(FILE_PATH):
        return []
    
    try:
        with open(FILE_PATH, "r", encoding='utf-8') as f:
            tasks = json.load(f)
            # Validate tasks structure
            return validate_tasks(tasks)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error loading tasks: {e}")
        # Create backup of corrupted file
        if os.path.exists(FILE_PATH):
            backup_path = f"{FILE_PATH}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(FILE_PATH, backup_path)
            print(f"Created backup of corrupted file: {backup_path}")
        return []
    except Exception as e:
        print(f"Unexpected error loading tasks: {e}")
        return []

def save_tasks(tasks):
    """Save tasks to JSON file with error handling and backup"""
    ensure_data_dir()
    
    try:
        # Create backup before saving
        if os.path.exists(FILE_PATH):
            backup_path = f"{FILE_PATH}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(FILE_PATH, backup_path)
        
        # Validate tasks before saving
        validated_tasks = validate_tasks(tasks)
        
        with open(FILE_PATH, "w", encoding='utf-8') as f:
            json.dump(validated_tasks, f, indent=4, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False

def validate_tasks(tasks):
    """Validate and fix task structure"""
    if not isinstance(tasks, list):
        return []
    
    validated_tasks = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
            
        # Ensure basic structure
        validated_task = {
            "title": task.get("title", "Untitled Task"),
            "done": task.get("done", False),
            "description": task.get("description", ""),
            "priority": task.get("priority", "medium"),
            "category": task.get("category", ""),
            "due_date": task.get("due_date", ""),
            "tags": task.get("tags", []),
            "created_at": task.get("created_at", datetime.now().isoformat()),
            "updated_at": task.get("updated_at", datetime.now().isoformat())
        }
        
        # Validate types
        if not isinstance(validated_task["tags"], list):
            validated_task["tags"] = []
        
        validated_tasks.append(validated_task)
    
    return validated_tasks

def export_tasks(tasks, filename):
    """Export tasks to a specific file"""
    try:
        export_data = {
            "export_date": datetime.now().isoformat(),
            "version": "1.0",
            "total_tasks": len(tasks),
            "tasks": validate_tasks(tasks)
        }
        
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(export_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error exporting tasks: {e}")
        return False

def import_tasks(filename):
    """Import tasks from a file"""
    try:
        if not os.path.exists(filename):
            return []
        
        with open(filename, "r", encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different export formats
        if isinstance(data, list):
            return validate_tasks(data)
        elif isinstance(data, dict) and "tasks" in data:
            return validate_tasks(data["tasks"])
        else:
            return []
    except Exception as e:
        print(f"Error importing tasks: {e}")
        return []

def get_task_statistics(tasks):
    """Calculate and return task statistics"""
    total = len(tasks)
    completed = len([t for t in tasks if t["done"]])
    pending = total - completed
    
    high_priority = len([t for t in tasks if t.get("priority") == "high" and not t["done"]])
    medium_priority = len([t for t in tasks if t.get("priority") == "medium" and not t["done"]])
    low_priority = len([t for t in tasks if t.get("priority") == "low" and not t["done"]])
    
    # Calculate overdue tasks
    overdue = 0
    for task in tasks:
        if task.get("due_date") and not task["done"]:
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                if due_date < datetime.now():
                    overdue += 1
            except ValueError:
                continue
    
    # Calculate completion percentage
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": completion_rate,
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "overdue": overdue
    }
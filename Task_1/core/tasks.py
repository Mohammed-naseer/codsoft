from datetime import datetime
import re

def add_task(task_list, title, description="", category="", priority="medium", due_date=None, tags=None):
    """
    Add a new task to the task list with advanced properties
    
    Args:
        task_list: List of existing tasks
        title: Task title (required)
        description: Task description
        category: Task category
        priority: Priority level (high/medium/low)
        due_date: Due date in YYYY-MM-DD format
        tags: List of tags
    
    Returns:
        Updated task list
    """
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")
    
    # Validate priority
    if priority not in ["high", "medium", "low"]:
        priority = "medium"
    
    # Validate due date format
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            due_date = None
    
    # Ensure tags is a list
    if tags is None:
        tags = []
    elif isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    task = {
        "title": title.strip(),
        "description": description.strip(),
        "category": category.strip(),
        "priority": priority,
        "due_date": due_date,
        "tags": tags,
        "done": False,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    task_list.append(task)
    return task_list

def delete_task(task_list, index):
    """
    Delete a task by index
    
    Args:
        task_list: List of tasks
        index: Index of task to delete
    
    Returns:
        Updated task list
    """
    if 0 <= index < len(task_list):
        task_list.pop(index)
    return task_list

def mark_done(task_list, index):
    """
    Mark a task as done
    
    Args:
        task_list: List of tasks
        index: Index of task to mark as done
    
    Returns:
        Updated task list
    """
    if 0 <= index < len(task_list):
        task_list[index]["done"] = True
        task_list[index]["updated_at"] = datetime.now().isoformat()
    return task_list

def mark_pending(task_list, index):
    """
    Mark a task as pending (not done)
    
    Args:
        task_list: List of tasks
        index: Index of task to mark as pending
    
    Returns:
        Updated task list
    """
    if 0 <= index < len(task_list):
        task_list[index]["done"] = False
        task_list[index]["updated_at"] = datetime.now().isoformat()
    return task_list

def toggle_task(task_list, index):
    """
    Toggle task completion status
    
    Args:
        task_list: List of tasks
        index: Index of task to toggle
    
    Returns:
        Updated task list
    """
    if 0 <= index < len(task_list):
        task_list[index]["done"] = not task_list[index]["done"]
        task_list[index]["updated_at"] = datetime.now().isoformat()
    return task_list

def update_task(task_list, index, **kwargs):
    """
    Update task properties
    
    Args:
        task_list: List of tasks
        index: Index of task to update
        **kwargs: Task properties to update
    
    Returns:
        Updated task list
    """
    if 0 <= index < len(task_list):
        task = task_list[index]
        
        # Update provided fields
        for key, value in kwargs.items():
            if key in task and key not in ["created_at", "updated_at"]:
                if key == "tags" and isinstance(value, str):
                    value = [tag.strip() for tag in value.split(",") if tag.strip()]
                task[key] = value
        
        task["updated_at"] = datetime.now().isoformat()
    
    return task_list

def filter_tasks(task_list, filter_type="all", search_term="", category="", priority=""):
    """
    Filter tasks based on various criteria
    
    Args:
        task_list: List of tasks to filter
        filter_type: all, pending, completed, overdue
        search_term: Text to search in title and description
        category: Filter by category
        priority: Filter by priority
    
    Returns:
        Filtered list of tasks
    """
    filtered_tasks = task_list.copy()
    
    # Apply status filter
    if filter_type == "pending":
        filtered_tasks = [task for task in filtered_tasks if not task["done"]]
    elif filter_type == "completed":
        filtered_tasks = [task for task in filtered_tasks if task["done"]]
    elif filter_type == "overdue":
        today = datetime.now().strftime("%Y-%m-%d")
        filtered_tasks = [task for task in filtered_tasks 
                         if task.get("due_date") and not task["done"] 
                         and task["due_date"] < today]
    
    # Apply search filter
    if search_term:
        search_term = search_term.lower()
        filtered_tasks = [task for task in filtered_tasks 
                         if (search_term in task["title"].lower() or 
                             search_term in task.get("description", "").lower())]
    
    # Apply category filter
    if category:
        filtered_tasks = [task for task in filtered_tasks 
                         if task.get("category", "").lower() == category.lower()]
    
    # Apply priority filter
    if priority:
        filtered_tasks = [task for task in filtered_tasks 
                         if task.get("priority", "").lower() == priority.lower()]
    
    return filtered_tasks

def sort_tasks(task_list, sort_by="created", reverse=False):
    """
    Sort tasks by various criteria
    
    Args:
        task_list: List of tasks to sort
        sort_by: created, due_date, priority, title, category
        reverse: Reverse sort order
    
    Returns:
        Sorted list of tasks
    """
    if not task_list:
        return task_list
    
    sorted_tasks = task_list.copy()
    
    # Priority order for sorting
    priority_order = {"high": 3, "medium": 2, "low": 1}
    
    def get_sort_key(task):
        if sort_by == "created":
            return task.get("created_at", "")
        elif sort_by == "due_date":
            due_date = task.get("due_date", "9999-12-31")  # Put tasks without due date last
            return due_date
        elif sort_by == "priority":
            return priority_order.get(task.get("priority", "medium"), 2)
        elif sort_by == "title":
            return task["title"].lower()
        elif sort_by == "category":
            return task.get("category", "").lower()
        else:
            return task.get("created_at", "")
    
    sorted_tasks.sort(key=get_sort_key, reverse=reverse)
    return sorted_tasks

def search_tasks(task_list, query):
    """
    Search tasks by title, description, tags, or category
    
    Args:
        task_list: List of tasks to search
        query: Search query
    
    Returns:
        List of matching tasks
    """
    if not query:
        return task_list
    
    query = query.lower()
    results = []
    
    for task in task_list:
        # Search in title
        if query in task["title"].lower():
            results.append(task)
            continue
        
        # Search in description
        if query in task.get("description", "").lower():
            results.append(task)
            continue
        
        # Search in category
        if query in task.get("category", "").lower():
            results.append(task)
            continue
        
        # Search in tags
        for tag in task.get("tags", []):
            if query in tag.lower():
                results.append(task)
                break
    
    return results

def get_categories(task_list):
    """
    Get all unique categories from task list
    
    Returns:
        List of unique categories
    """
    categories = set()
    for task in task_list:
        if task.get("category"):
            categories.add(task["category"])
    return sorted(categories)

def get_tasks_by_category(task_list, category):
    """
    Get tasks filtered by category
    
    Returns:
        List of tasks in the specified category
    """
    return [task for task in task_list if task.get("category") == category]

def clear_completed_tasks(task_list):
    """
    Remove all completed tasks from the list
    
    Returns:
        Updated task list with only pending tasks
    """
    return [task for task in task_list if not task["done"]]

def duplicate_task(task_list, index):
    """
    Duplicate a task
    
    Returns:
        Updated task list with duplicated task
    """
    if 0 <= index < len(task_list):
        original_task = task_list[index]
        new_task = original_task.copy()
        new_task["title"] = f"{original_task['title']} (Copy)"
        new_task["created_at"] = datetime.now().isoformat()
        new_task["updated_at"] = datetime.now().isoformat()
        new_task["done"] = False
        task_list.insert(index + 1, new_task)
    
    return task_list

def validate_task_data(task):
    """
    Validate task data structure
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not isinstance(task, dict):
        return False, "Task must be a dictionary"
    
    if "title" not in task or not task["title"].strip():
        return False, "Task title is required"
    
    if not isinstance(task.get("done", False), bool):
        return False, "Done status must be boolean"
    
    if "priority" in task and task["priority"] not in ["high", "medium", "low"]:
        return False, "Priority must be high, medium, or low"
    
    if "due_date" in task and task["due_date"]:
        try:
            datetime.strptime(task["due_date"], "%Y-%m-%d")
        except ValueError:
            return False, "Due date must be in YYYY-MM-DD format"
    
    return True, "Valid"
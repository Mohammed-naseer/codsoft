from datetime import datetime

def add_task(task_list, title, description="", category="", priority="medium", due_date=None, tags=None):
    task = {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "tags": tags or [],
        "done": False,
        "created_at": datetime.now().isoformat()
    }
    task_list.append(task)
    return task_list

def toggle_task(task_list, index):
    if 0 <= index < len(task_list):
        task_list[index]["done"] = not task_list[index]["done"]
        task_list[index]["updated_at"] = datetime.now().isoformat()
    return task_list

def delete_task(task_list, index):
    if 0 <= index < len(task_list):
        task_list.pop(index)
    return task_list
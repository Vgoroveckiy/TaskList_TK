import json
import os
from datetime import datetime
import tkinter as tk

def save_data(listbox1, listbox2, listbox3):
    """Сохраняет данные из списков в JSON файл"""
    data = {
        "backlog": [listbox1.task_data[i] for i in range(listbox1.size())],
        "in_progress": [listbox2.task_data[i] for i in range(listbox2.size())],
        "done": [listbox3.task_data[i] for i in range(listbox3.size())]
    }
    
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(listbox1, listbox2, listbox3):
    """Загружает данные из JSON файла в списки"""
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
                for task in data["backlog"]:
                    # Поддерживаем старый и новый формат данных
                    title = task.get("title", task.get("text", ""))
                    listbox1.insert("end", title)
                    # Обновляем данные задачи до нового формата
                    task_data = {
                        "title": title,
                        "description": task.get("description", ""),
                        "priority": task.get("priority", ""),
                        "assignee": task.get("assignee", ""),
                        "deadline": task.get("deadline", ""),
                        "modified": task.get("modified", ""),
                        "modified_by": task.get("modified_by", "")
                    }
                    listbox1.task_data.append(task_data)
                
                for task in data["in_progress"]:
                    title = task.get("title", task.get("text", ""))
                    listbox2.insert("end", title)
                    task_data = {
                        "title": title,
                        "description": task.get("description", ""),
                        "priority": task.get("priority", ""),
                        "assignee": task.get("assignee", ""),
                        "deadline": task.get("deadline", ""),
                        "modified": task.get("modified", ""),
                        "modified_by": task.get("modified_by", "")
                    }
                    listbox2.task_data.append(task_data)
                
                for task in data["done"]:
                    title = task.get("title", task.get("text", ""))
                    listbox3.insert("end", title)
                    task_data = {
                        "title": title,
                        "description": task.get("description", ""),
                        "priority": task.get("priority", ""),
                        "assignee": task.get("assignee", ""),
                        "deadline": task.get("deadline", ""),
                        "modified": task.get("modified", ""),
                        "modified_by": task.get("modified_by", "")
                    }
                    listbox3.task_data.append(task_data)
        except json.JSONDecodeError:
            pass

def add_task(entry, listbox, save_callback, current_user, task_data):
    """Добавляет новую задачу в список"""
    if task_data["title"]:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_data.update({
            "modified": current_time,
            "modified_by": current_user
        })
        listbox.insert("end", task_data["title"])
        listbox.task_data.append(task_data)
        save_callback()

def edit_task(listbox, index, new_data, save_callback, current_user):
    """Редактирует существующую задачу"""
    if new_data["title"]:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data.update({
            "modified": current_time,
            "modified_by": current_user
        })
        listbox.delete(index)
        listbox.insert(index, new_data["title"])
        listbox.task_data[index] = new_data
        save_callback()

def move_right(source_listbox, target_listbox, save_callback, current_user):
    """Перемещает выбранную задачу вправо"""
    selection = source_listbox.curselection()
    if selection:
        index = selection[0]
        task_data = source_listbox.task_data[index]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_data.update({
            "modified": current_time,
            "modified_by": current_user
        })
        
        target_listbox.insert("end", task_data["title"])
        target_listbox.task_data.append(task_data)
        
        source_listbox.delete(index)
        source_listbox.task_data.pop(index)
        save_callback()

def move_left(source_listbox, target_listbox, save_callback, current_user):
    """Перемещает выбранную задачу влево"""
    selection = source_listbox.curselection()
    if selection:
        index = selection[0]
        task_data = source_listbox.task_data[index]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_data.update({
            "modified": current_time,
            "modified_by": current_user
        })
        
        target_listbox.insert("end", task_data["title"])
        target_listbox.task_data.append(task_data)
        
        source_listbox.delete(index)
        source_listbox.task_data.pop(index)
        save_callback()

def delete_task(listbox, save_callback):
    """Удаляет выбранную задачу"""
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        listbox.delete(index)
        listbox.task_data.pop(index)
        save_callback()

def get_task_info(listbox):
    """Возвращает информацию о выбранной задаче"""
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        if index < len(listbox.task_data):
            return listbox.task_data[index]
    return None

def get_users_list():
    """Возвращает список всех пользователей из users.json"""
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                users_data = json.load(f)
                # Проверяем формат данных
                if isinstance(users_data, dict):
                    # Если это словарь, возвращаем ключи (имена пользователей)
                    return list(users_data.keys())
                elif isinstance(users_data, list):
                    # Если это список, извлекаем имена пользователей
                    return [user.get("username") for user in users_data if isinstance(user, dict)]
                return []
        except json.JSONDecodeError:
            return []
    return [] 
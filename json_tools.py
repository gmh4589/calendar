
import os
import json


class BaseTools:
    _instance = None

    def __init__(self, json_file="todo_list.json"):
        self.json_file = json_file
        self.data = self._load_data()

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(BaseTools, cls).__new__(cls)

        return cls._instance

    def _load_data(self):

        if os.path.exists(self.json_file):

            with open(self.json_file, "r", encoding="utf-8") as f:
                return json.load(f)

        return {}

    def _save_data(self):

        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def create_table(self, date):

        if date not in self.data:
            self.data[date] = []
            self._save_data()

    def add_task(self, date, task, completed=0):

        self.create_table(date)
        tasks = self.data[date]
        new_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
        # print(task, new_id)

        tasks.append({
            "id": new_id,
            "task": task,
            "completed": completed
        })
        self._save_data()

        return new_id, len(tasks)

    def complete_task(self, date, task_id, completed=1):
        tasks = self.data.get(date, [])

        for task in tasks:

            if task["id"] == task_id:
                task["completed"] = completed
                break

        self._save_data()

    def delete_task(self, date, task_id):

        if date in self.data:
            self.data[date] = [task for task in self.data[date] if task["id"] != task_id]
            self._save_data()

    def edit_task(self, date, task_id, new_text):
        tasks = self.data.get(date, [])
        # print(task_id, new_text)

        for task in tasks:

            if task["id"] == task_id:
                task["task"] = new_text
                break

        self._save_data()

    def get_tasks(self, date):
        return self.data.get(date, [])

from dataclasses import dataclass, field, asdict
from src.task import Task
from typing import List
from pathlib import Path
import datetime
import json

@dataclass
class TaskTracker:
    unique_id: int = 0
    directory: Path = field(default_factory=lambda: Path.cwd() / "tasks.json")
    tasks: List[Task] = field(default_factory=list)
    database: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.directory.exists():
            self.database = {}
            with open(self.directory, "w") as write_file:
                json.dump(self.database, write_file)
        else:
            with open(self.directory, "r") as read_file:
                self.database = json.load(read_file)
            self.unique_id = self.database["id"]
            self.tasks = [Task(**t) for t in self.database]

    @staticmethod
    def _format_datetime(date: datetime.datetime) -> str:
        return date.strftime("%a %d %b %Y, %H:%M")

    def add(self, description: str) -> str:
        if description.strip() == "":
            raise ValueError(f"Description must not be empty.")
        
        task_id: int = self.unique_id
        task = Task(id=task_id, description=description)
        self.tasks.append(task)

        # build/update the database dict 
        self.database[task_id] = asdict(task)
        self.unique_id += 1
        self.save()
        return f"Task added successfully (ID: {task_id})"

    def update(self, id: int, description: str) -> None:
        ids: List[int] = [task.id for task in self.tasks]
        if description.strip() == "":
            raise ValueError(f"Description must not be empty.")
        if id not in ids:
            raise ValueError(f"Task with the ID: {id} is not in the task list.")
        for task in self.tasks:
            if task.id == id:
                task.description = description
                task.updatedAt = self._format_datetime(datetime.datetime.now())

    def delete(self, id: int) -> None:
        ids: List[int] = [task.id for task in self.tasks]
        if id not in ids:
            raise ValueError(f"Task with the ID: {id} is not in the task list.")
        for idx, task in enumerate(self.tasks):
            if task.id == id:
                self.tasks.pop(idx)

    def change_status(self, id: int, status: str) -> None:
        ids: List[int] = [task.id for task in self.tasks]
        if id not in ids:
            raise ValueError(f"Task with the ID: {id} is not in the task list.")
        if status not in ["in-progress", "done"]:
            raise ValueError(f"Status must be either of (\"in-progress\", \"done\").")
        for task in self.tasks:
            if task.id == id:
                task.status = status
                task.updatedAt = self._format_datetime(datetime.datetime.now())
    
    def list(self, status: str = "all") -> str:
        if status in ["done", "todo", "in-progress"]:
            tasks = [task for task in self.tasks if task.status == status]
        else:
            tasks = self.tasks
        return "\n".join(repr(task) for task in tasks)
    
    def save(self) -> None:
        with open(self.directory, "w") as write_file:
            json.dump(self.database, write_file)
    


            
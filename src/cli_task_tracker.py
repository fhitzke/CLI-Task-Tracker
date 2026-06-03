from dataclasses import dataclass, field, asdict
from src.task import Task
from typing import List, Tuple
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
            if  len(self.database) == 0:
                self.unique_id = 0
            else:
                self.unique_id = int(list(self.database.keys())[-1]) + 1
            self.tasks = [
                Task(**{
                    **t,
                    "createdAt": datetime.datetime.strptime(t["createdAt"], "%a %d %b %Y, %H:%M"),
                    "updatedAt": datetime.datetime.strptime(t["updatedAt"], "%a %d %b %Y, %H:%M"),
                }) for t in self.database.values()
            ]

    @staticmethod
    def _format_datetime(date: datetime.datetime) -> str:
        return date.strftime("%a %d %b %Y, %H:%M")
    
    def save(self) -> None:
        try:
            with open(self.directory, "w") as write_file:
                json.dump(self.database, write_file)
        except OSError as e: 
            raise OSError(f"Failed to write file: {e}")
        except TypeError as e:
            raise TypeError(f"Database contains non-serializable data: {e}")
        
    def purge_task_registry(self) -> None:
        try:
            self.database = {}
            with open(self.directory, "w") as write_file:
                json.dump(self.database, write_file)
        except OSError as e:
            raise OSError(f"Failed to write file: {e}")
    
    def get_task(self, id: int) -> Tuple[int, Task]:
        ids: List[int] = [task.id for task in self.tasks]
        if id not in ids:
            raise ValueError(f"Task with the id: {id} is not in the task list.")
        for task_idx, task in enumerate(self.tasks):
            if task.id == id:
                return (task_idx, task)

    def add(self, description: str) -> str:
        if description.strip() == "":
            raise ValueError(f"Description must not be empty.")
        task_id: int = self.unique_id
        task = Task(id=task_id, description=description)
        self.tasks.append(task)
        self.database[str(task_id)] = asdict(task)
        self.unique_id += 1
        # NOTE: unique_id is incremented here so that multiple calls to add()
        # within the same session assign unique IDs.
        # The CLI only calls add() once per process, so __post_init__ alone would suffice
        # but tests reuse the same tracker instance.
        self.save()
        return f"Task added successfully (ID: {task_id})"

    def update(self, id: int, description: str) -> str:
        if description.strip() == "":
            raise ValueError(f"Description must not be empty.")
        task = self.get_task(id)[1]
        task.description = description
        task.updatedAt = self._format_datetime(datetime.datetime.now())
        self.database[str(task.id)] = asdict(task)
        self.save()
        return f"Description of Task ({task.id}) updated to: \"{task.description}\""

    def delete(self, id: int) -> str:
        task = self.get_task(id)
        self.tasks.pop(task[0])
        del self.database[str(task[1].id)]
        self.save()
        return f"Removed Task ({task[1].id}): \"{task[1].description}\""

    def change_status(self, id: int, status: str) -> str:
        if status not in ["in-progress", "done"]:
            raise ValueError(f"Status must be either of (\"in-progress\", \"done\").") # TODO: graceful handling
        task = self.get_task(id)[1]
        task.status = status
        task.updatedAt = self._format_datetime(datetime.datetime.now())
        self.database[str(task.id)] = asdict(task)
        self.save()
        return f"Status of Task ({task.id}): \"{task.description}\" changed to: \"{task.status}\""

    def list(self, status: str = "all") -> str:
        if status in ["done", "todo", "in-progress"]:
            tasks = [task for task in self.tasks if task.status == status]
        else:
            tasks = self.tasks
        return "\n".join(repr(task) for task in tasks)
    


            
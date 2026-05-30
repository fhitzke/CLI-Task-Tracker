from src.task import Task
from src.cli_task_tracker import TaskTracker

def main():
    task_tracker = TaskTracker()
    print(task_tracker.add("Buy groceries"))
    print(task_tracker.add("Walk the dog"))

    # print(task_tracker.list())

    # task_tracker.update(0, "Buy groceries and cook dinner")

    # print(task_tracker.list("todo"))

    # task_tracker.delete(0)

    # print(task_tracker.list())

    # task_tracker.change_status(1, "done")

    # print(task_tracker.list("done"))
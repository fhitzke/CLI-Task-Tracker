from src.task import Task
from src.cli_task_tracker import TaskTracker
import argparse

def main():
    task_tracker = TaskTracker()
    parser = argparse.ArgumentParser(description="A simple CLI Task Tracker application")
    subparsers = parser.add_subparsers(dest="command", required=True, help="task commands")

    # adding tasks
    add_parser = subparsers.add_parser("add", help="Add a task to the task registry by passing a description.")
    add_parser.add_argument("description", type=str)
    add_parser.set_defaults(func=lambda args: print(task_tracker.add(args.description)))

    # updating tasks
    update_parser = subparsers.add_parser("update", help="Update the description of a task, by passing the task id and new description.")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("description", type=str)
    update_parser.set_defaults(func=lambda args: print(task_tracker.update(args.id, args.description)))

    # deleting tasks
    delete_parser = subparsers.add_parser("delete", help="Delete a task by passing the task id.")
    delete_parser.add_argument("id", type=int)
    delete_parser.set_defaults(func=lambda args: print(task_tracker.delete(args.id)))

    # changing status
    status_parser = subparsers.add_parser("status", help="Change a task's status by passing the task id and new status.")
    status_parser.add_argument("id", type=int)
    status_parser.add_argument("status", type=str)
    status_parser.set_defaults(func=lambda args: print(task_tracker.change_status(args.id, args.status)))

    # list tasks
    list_parser = subparsers.add_parser("list", help="List all tasks with the specified status. None lists all tasks.")
    list_parser.add_argument("status", nargs="?", default="all")
    list_parser.set_defaults(func=lambda args: print(task_tracker.list(args.status)))

    args = parser.parse_args()
    args.func(args)
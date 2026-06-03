from src.cli_task_tracker import TaskTracker
from pathlib import Path
from unittest.mock import patch
import pytest
import datetime
import json
import re

def test_task_tracker_creates_directory_if_none_exists():
    pass

def test_task_tracker_reads_from_the_right_directory():
    tracker = TaskTracker()
    directory = tracker.directory
    expected_directory = Path("/Users/fhitzke/Desktop/CLI-Task-Tracker/tasks.json")
    assert directory == expected_directory

def test_task_tracker_reads_database_correctly_from_directory():
    tracker = TaskTracker()
    database = tracker.database
    with open(Path("/Users/fhitzke/Desktop/CLI-Task-Tracker/tasks.json")) as read_file:
        expected_database = json.load(read_file)
    assert database == expected_database

def test_adding_task_with_empty_description_raises_value_error():
    tracker = TaskTracker()
    with pytest.raises(ValueError):
        tracker.add("")
    tracker.purge_task_registry()

def test_unique_id_increments_correctly_after_add():
    tracker = TaskTracker()
    init_unique_id = tracker.unique_id
    tracker.add("Do something")
    unique_id_after_add = tracker.unique_id
    assert unique_id_after_add == init_unique_id + 1
    tracker.purge_task_registry()

def test_add_return_string_contains_correct_id():
    tracker = TaskTracker()
    result = tracker.add("Do something")
    match = re.search(r"ID: (\d+)", result)
    assert match is not None
    assert int(match.group(1)) == tracker.tasks[0].id
    tracker.purge_task_registry()

def test_get_task_returns_correct_tuple():
    tracker = TaskTracker()
    tracker.add("Do something")
    returned_tuple = tracker.get_task(0)
    expected_tuple = (0, tracker.tasks[0])
    assert returned_tuple == expected_tuple
    tracker.purge_task_registry()

def test_get_task_returns_correct_task():
    tracker = TaskTracker()
    tracker.add("Do something")
    returned_task = tracker.get_task(0)[1]
    expected_task = tracker.tasks[0]
    assert returned_task == expected_task
    tracker.purge_task_registry()

def test_get_task_raises_value_error_on_non_existent_id():
    tracker = TaskTracker()
    tracker.add("Do something")
    with pytest.raises(ValueError):
        tracker.get_task(1)
    tracker.purge_task_registry()

def test_update_with_empty_description_raises_value_error():
    tracker = TaskTracker()
    tracker.add("Do something")
    with pytest.raises(ValueError):
        tracker.update(0, "")
    tracker.purge_task_registry()

def test_updating_a_non_existent_id_raises_value_error():
    tracker = TaskTracker()
    tracker.add("Do something")
    with pytest.raises(ValueError):
        tracker.update(1, "")
    tracker.purge_task_registry()

def test_update_correctly_updates_task_description():
    tracker = TaskTracker()
    tracker.add("Do something")
    new_description = "Something else"
    tracker.update(0, new_description)
    assert tracker.tasks[0].description == new_description
    tracker.purge_task_registry()

def test_update_correctly_sets_updatedAt():
    tracker = TaskTracker()
    tracker.add("Do something")
    initial_updatedAt = tracker.tasks[0].updatedAt
    future = datetime.datetime(2050, 1, 1, 12, 00)
    with patch("src.cli_task_tracker.datetime.datetime") as mock_dt:
        mock_dt.now.return_value = future
        mock_dt.strftime = datetime.datetime.strftime
        tracker.update(0, "Something else")
    assert tracker.tasks[0].updatedAt != initial_updatedAt
    assert tracker.tasks[0].updatedAt == "Sat 01 Jan 2050, 12:00"
    tracker.purge_task_registry()

def test_delete_deletes_correct_task():
    tracker = TaskTracker()
    tracker.add("Do something")
    tracker.add("Do something else")
    task_id = tracker.tasks[0].id
    tracker.delete(task_id)
    remaining_ids = [task.id for task in tracker.tasks]
    assert task_id not in remaining_ids
    tracker.purge_task_registry()

def test_deleting_a_non_existent_id_raises_value_error():
    tracker = TaskTracker()
    tracker.add("Do something")
    with pytest.raises(ValueError):
        tracker.delete(1)
    tracker.purge_task_registry()

def test_task_list_length_shrinks_by_one_after_delete():
    tracker = TaskTracker()
    tracker.add("Do something")
    before = len(tracker.tasks)
    tracker.delete(0)
    assert len(tracker.tasks) == before - 1

def test_database_does_not_contain_deleted_key_after_reload():
    tracker = TaskTracker()
    tracker.add("Do something")
    task_id = str(tracker.tasks[0].id)
    tracker.delete(tracker.tasks[0].id)
    tracker.save()
    tracker = TaskTracker()
    assert task_id not in tracker.database
    tracker.purge_task_registry()

def test_invalid_status_in_change_status_raises_value_error():
    tracker = TaskTracker()
    tracker.add("Do something")
    with pytest.raises(ValueError):
        tracker.change_status(0, "garbage")
    tracker.purge_task_registry()

def test_change_status_status_can_be_set_to_values():
    tracker = TaskTracker()
    tracker.add("Do something")
    tracker.add("Do something")
    in_progress = "in-progress"
    done = "done"
    tracker.change_status(0, in_progress)
    tracker.change_status(1, done)
    assert tracker.tasks[0].status == "in-progress"
    assert tracker.tasks[1].status == "done"
    tracker.purge_task_registry()

def test_change_status_sets_correct_status():
    tracker = TaskTracker()
    tracker.add("Do something")
    task_status = "done"
    tracker.change_status(0, task_status)
    assert tracker.tasks[0].status == task_status
    tracker.purge_task_registry()

def test_list_returns_all_tasks_called_with_no_arguments():
    tracker = TaskTracker()
    tracker.add("Do something")
    tracker.add("Do something else")
    number_of_tasks = len(tracker.tasks)
    result = tracker.list()
    matches = re.findall(r"Task \((\d+)\):", result)
    assert len(matches) == number_of_tasks
    tracker.purge_task_registry()

def test_list_output_filtering_works():
    tracker = TaskTracker()
    tracker.add("This")
    tracker.add("is")
    tracker.add("a")
    tracker.add("test")
    tracker.change_status(0, "done")
    done_task = tracker.tasks[0]
    expected_output = repr(done_task)
    assert tracker.list("done") == expected_output
    tracker.purge_task_registry()

def test_returns_empty_string_when_no_tasks_match_filter():
    tracker = TaskTracker()
    tracker.add("Do something")
    tracker.add("Do something else")
    result = tracker.list("done")
    assert result == ""

def test_task_id_is_int_after_reload():
    tracker = TaskTracker()
    tracker.add("Do something")
    tracker.save()

    tracker = TaskTracker()
    assert isinstance(tracker.tasks[0].id, int)
    tracker.purge_task_registry()

def test_task_list_is_restored_correctly():
    tracker = TaskTracker()
    tracker.add("Do something")
    task_list = tracker.tasks
    tracker.save()

    tracker = TaskTracker()
    restored_task_list = tracker.tasks
    assert task_list == restored_task_list
    tracker.purge_task_registry()

def test_database_is_restored_correctly():
    tracker = TaskTracker()
    tracker.add("Do something")
    database = tracker.database
    tracker.save()

    tracker = TaskTracker()
    restored_database = tracker.database
    assert database == restored_database
    tracker.purge_task_registry()


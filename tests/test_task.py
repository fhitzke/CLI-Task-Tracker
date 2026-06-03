from src.task import Task
import datetime

def test_task_fields():
    task = Task(id=1, description="This is a test")
    assert task.id == 1
    assert task.description == "This is a test"
    assert task.status == "todo" # default status must be "todo"
    assert task.createdAt == datetime.datetime.now().strftime("%a %d %b %Y, %H:%M") 
    assert task.updatedAt == datetime.datetime.now().strftime("%a %d %b %Y, %H:%M") # default for both createdAt/updatedAt is now()

# default "todo" status is always enforced
def test_task_status_cannot_be_set_manually():
    task = Task(id=1, description="This is a test", status="garbage")
    assert task.status == "todo"

# task repr is as expected
def test_task_repr():
    task = Task(id=1, description="This is a test")
    expected = f"Task (1): \"This is a test\" | Status: \"todo\" | Updated: \"{task.updatedAt}\""
    assert repr(task) == expected

# post_init converts datetime to str
def test_task_dates_are_strings_after_init():
    task = Task(id=1, description="This is a test")
    assert isinstance(task.createdAt, str)
    assert isinstance(task.updatedAt, str)

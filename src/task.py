from dataclasses import dataclass, field
import datetime

@dataclass
class Task:
    id: int
    description: str
    status: str = field(default="todo")
    createdAt: datetime.datetime = field(default_factory=datetime.datetime.now)
    updatedAt: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __repr__(self):
        return f"Task ({self.id}): \"{self.description}\" | Status: \"{self.status}\" | Updated: \"{self.updatedAt}\""
    
    def __post_init__(self):
        self.status = "todo"
        self.updatedAt = self.updatedAt.strftime("%a %d %b %Y, %H:%M")
        self.createdAt = self.createdAt.strftime("%a %d %b %Y, %H:%M")
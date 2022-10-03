from typing import Callable, Optional
from ..utils import Parser
from .model import Model


class Todo(Model):
    fields = ["about", "due", "urgency"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)

        self.about = ""
        self.due = "today"
        self.urgency = 4
        self.status = "PENDING"
        self.ctype = type(self)

        self.opts = {
            "PENDING": "x",
            "COMPLETED": "X",
            "OVERDUE": "O",
        }

    def to_data(self) -> str:

        # status = self.opts[self.status]
        return f"{self.status} ({self.urgency}) due:{self.due or 'None'} {self.about}"

    def fill_from_data(self, data: str):
        status, urgency, due, *about = data.split()

        # status = self.opts[status]
        about = " ".join(about)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        self.about = about
        self.urgency = urgency
        self.date = due
        self.status = status

    def commit(self):
        return [self.to_data(), [child.commit() for child in self.children]]

    def from_data(self, data):
        for i, j in data:
            self.add_child()
            self.children[-1].fill_from_data(i)
            self.children[-1].from_export(j)


class Topic(Model):
    fields = ["about"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.about = ""
        self.ctype: Callable = Todo

    def commit(self):
        return [child.export() for child in self.children]

    def from_data(self, data):
        for i, j in data:
            self.add_child()
            self.children[-1].fill_from_data(i)
            self.children[-1].from_data(j)


class Workspace(Model):
    fields = ["about"]
    nomenclature: str = "Topic"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.about = ""
        self.ctype: Callable = Topic


class Manager(Model):
    fields = []
    nomenclature: str = "Workspace"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.ctype: Callable = Workspace

    def commit(self):
        data = super().commit()
        Parser.save(data)

    def setup(self):
        data = Parser.load()
        self.from_data(data)


manager = Manager(name="Manager")
manager.setup()
# for i in range(5):
#     manager.add_child()
#     manager.children[-1].add_child()
#     manager.children[-1].children[-1].add_child()

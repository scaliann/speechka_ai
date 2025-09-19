from enum import Enum as PyEnum


class SessionStatus(PyEnum):
    active = "active"
    completed = "completed"
    aborted = "aborted"

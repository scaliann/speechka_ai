from enum import Enum as PyEnum


class SessionStatus(PyEnum):
    active = "active"
    completed = "completed"
    aborted = "aborted"


class DiagnosisResult(PyEnum):
    healthy = "healthy"
    burr = "burr"
    lisp = "lisp"
    burr_lisp = "burr-lisp"

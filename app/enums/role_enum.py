from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    GUEST = "guest"
    LIBRARIAN = "librarian"

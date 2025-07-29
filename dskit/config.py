from typing import Optional

TARGET: Optional[str] = None


def set_target(name: str):
    global TARGET
    TARGET = name


def get_target() -> str:
    return TARGET

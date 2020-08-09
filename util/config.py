import enum

import util

class TaskLevel(enum.Enum):
    TASK = enum.auto()
    FULL = enum.auto()

task_config = {}
task_level = TaskLevel.TASK

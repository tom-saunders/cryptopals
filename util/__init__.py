import util.config

_current_max_set = 1

def memoize(f):
    cache = {}

    def memoized_func(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    memoized_func.cache = cache
    return memoized_func

def get_tasks():
    return util.config.tasks

def get_task_level():
    return util.config.task_level

def set_task_level(level):
    if level.lower() == 'full':
        util.config.task_level = util.config.TaskLevel.FULL
    elif level.lower() == 'task':
        util.config.task_level = util.config.TaskLevel.TASK
    else:
        print('invalid value set for level, assume TASK')
        util.config.task_level = util.config.TaskLevel.TASK

def set_tasks(tasks_arg = None):
    tasks = {}
    if tasks_arg == None:
        for set_num in range(1, _current_max_set + 1):
            tasks[set_num] = {}
            for task_num in range(1, 9):
                tasks[set_num][task_num] = True
        util.config.tasks = tasks
    else:
        for set_num in range(1, _current_max_set + 1):
            tasks[set_num] = {}
            for task_num in range(1, 9):
                tasks[set_num][task_num] = False
        for task_str in tasks_arg:
            split_task = task_str.split(':')
            task_elements = len(split_task)
            set_num = int(split_task[0])
            if task_elements == 1:
                for task_num in range(1, 9):
                    tasks[set_num][task_num] = True
            elif task_elements == 2:
                task_nums_strs = split_task[1].split(',')
                for task_nums_str in task_nums_strs:
                    task_nums_range = task_nums_str.split('-')
                    task_nums_elements = len(task_nums_range)
                    if task_nums_elements == 1:
                        tasks[set_num][int(task_nums_range[0])] = True
                    elif task_nums_elements == 2:
                        start = int(task_nums_range[0])
                        end = int(task_nums_range[1])
                        if start >= end:
                            # ????
                            pass
                        if end > 8:
                            # ????
                            pass
                        else:
                            for task_num in range(start, end + 1):
                                tasks[set_num][task_num] = True
                    else:
                        # ????
                        pass
            else:
                # ????
                pass
            util.config.tasks = tasks



import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][8], 'test not set to run')
@unittest.skipUnless(util.get_task_level() == util.config.TaskLevel.FULL, 'full test not set to run')
class S1_T8_full(unittest.TestCase):
    def test(self):
        pass
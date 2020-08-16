import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][3], 'test not set to run')
@unittest.skipUnless(util.get_task_level() == util.config.TaskLevel.FULL, 'full test not set to run')
class S1_T3_full(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T3_full, self).__init__(*args, **kwargs)

    def test(self):
        self.skipTest('[{}] unimplemented'.format(str(self)))

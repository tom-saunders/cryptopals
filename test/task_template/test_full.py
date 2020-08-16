#import unittest
#
#import util
#
#@unittest.skipUnless(util.get_tasks()[x][y], 'test not set to run')
#@unittest.skipUnless(util.get_task_level() == util.config.TaskLevel.FULL, 'full test not set to run')
#class Sx_Ty_full(unittest.TestCase):
#    def __init__(self, *args, **kwargs):
#        super(Sx_Ty_full, self).__init__(*args, **kwargs)
#
#    def test(self):
#        self.skipTest('[{}] unimplemented'.format(str(self)))

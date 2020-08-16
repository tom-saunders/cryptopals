import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][7], 'test not set to run')
class S1_T7_main(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T7_main, self).__init__(*args, **kwargs)

    def test(self):
        self.skipTest('[{}] unimplemented'.format(str(self)))

import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][2], 'test not set to run')
class S1_T2_main(unittest.TestCase):
    def test(self):
        pass

import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][3], 'test not set to run')
class S1_T3_main(unittest.TestCase):
    def test(self):
        pass
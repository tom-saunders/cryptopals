import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][4], 'test not set to run')
class S1_T4_main(unittest.TestCase):
    def test(self):
        pass

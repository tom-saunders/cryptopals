import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][7], 'test not set to run')
class S1_T7_main(unittest.TestCase):
    def test(self):
        pass

import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][1], 'test not set to run')
class S1_T1_main(unittest.TestCase):
    def test(self):
        pass

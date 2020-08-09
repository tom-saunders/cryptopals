import unittest

import util

@unittest.skipUnless(util.get_tasks()[1][6], 'test not set to run')
class S1_T6_main(unittest.TestCase):
    def test(self):
        pass

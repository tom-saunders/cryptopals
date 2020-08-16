import unittest

import util
import util.xor

@unittest.skipUnless(util.get_tasks()[1][2], 'test not set to run')
class S1_T2_main(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T2_main, self).__init__(*args, **kwargs)
        self.left_hex  = '1c0111001f010100061a024b53535009181c'
        self.left  = bytes.fromhex(self.left_hex)
        self.right_hex = '686974207468652062756c6c277320657965'
        self.right  = bytes.fromhex(self.right_hex)
        self.expected_hex = '746865206b696420646f6e277420706c6179'
        self.expected  = bytes.fromhex(self.expected_hex)

    def test_xor(self):
        actual = util.xor.fixed(self.left, self.right)
        self.assertEqual(self.expected, actual)

        derived_left = util.xor.fixed(actual, self.right)
        self.assertEqual(self.left, derived_left)

        derived_right = util.xor.fixed(actual, self.left)
        self.assertEqual(self.right, derived_right)

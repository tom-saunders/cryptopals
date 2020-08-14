import unittest

import util
import util.base64

@unittest.skipUnless(util.get_tasks()[1][1], 'test not set to run')
class S1_T1_main(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T1_main, self).__init__(*args, **kwargs)
        self.predefined_input = bytes.fromhex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
        self.expected_output = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

    def test_encode(self):
        actual_output = util.base64.encode(self.predefined_input)
        self.assertEqual(self.expected_output, actual_output, 'base64 encode produces incorrect output')

    def test_decode(self):
        dec_expected_output = util.base64.decode(self.expected_output)
        self.assertEqual(self.predefined_input, dec_expected_output, 'base64 decode produces incorrect output')

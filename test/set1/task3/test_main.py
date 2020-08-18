import unittest
import decimal

import util.xor
import util.weighting

@unittest.skipUnless(util.get_tasks()[1][3], 'test not set to run')
class S1_T3_main(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T3_main, self).__init__(*args, **kwargs)
        self.input_hex = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
        self.input = bytes.fromhex(self.input_hex)

    def test(self):
        possible_keys = [bytes([x]) for x in range(0,256)]
        possible_decrypts = {}
        for possible_key in possible_keys:
            candidate_decrypt = util.xor.repeated_bytes(self.input, possible_key)
            possible_decrypts[possible_key] = candidate_decrypt

        self.assertEqual(True, False)

import unittest

import util
import util.base64
from util.base64.impl import Base64Exception

@unittest.skipUnless(util.get_tasks()[1][1], 'test not set to run')
@unittest.skipUnless(util.get_task_level() == util.config.TaskLevel.FULL, 'full test not set to run')
class S1_T1_full(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T1_full, self).__init__(*args, **kwargs)

    def test_valid_decode(self):
        valid_inputs = {
            ''   : b'',
            '8A' : b'\xf0',
            '8Q' : b'\xf1',
            '8g' : b'\xf2',
            '8w' : b'\xf3',
            '//A': b'\xff\xf0',
            '//E': b'\xff\xf1',
            '//I': b'\xff\xf2',
            '//M': b'\xff\xf3',
            '//Q': b'\xff\xf4',
            '//U': b'\xff\xf5',
            '//Y': b'\xff\xf6',
            '//c': b'\xff\xf7',
            '//g': b'\xff\xf8',
            '//k': b'\xff\xf9',
            '//o': b'\xff\xfa',
            '//s': b'\xff\xfb',
            '//w': b'\xff\xfc',
            '//0': b'\xff\xfd',
            '//4': b'\xff\xfe',
            '//8': b'\xff\xff',
            'AA' : b'\x00',
            'BA' : b'\x04',
            'CA' : b'\x08',
            'DA' : b'\x0c',
            'EA' : b'\x10',
            'FA' : b'\x14',
            'GA' : b'\x18',
            'HA' : b'\x1c',
            'IA' : b'\x20',
            'JA' : b'\x24',
            'KA' : b'\x28',
            'LA' : b'\x2c',
            'MA' : b'\x30',
            'NA' : b'\x34',
            'OA' : b'\x38',
            'PA' : b'\x3c',
            'QA' : b'\x40',
            'RA' : b'\x44',
            'SA' : b'\x48',
            'TA' : b'\x4c',
            'UA' : b'\x50',
            'VA' : b'\x54',
            'WA' : b'\x58',
            'XA' : b'\x5c',
            'YA' : b'\x60',
            'ZA' : b'\x64',
            'aA' : b'\x68',
            'bA' : b'\x6c',
            'cA' : b'\x70',
            'dA' : b'\x74',
            'eA' : b'\x78',
            'fA' : b'\x7c',
            'gA' : b'\x80',
            'hA' : b'\x84',
            'iA' : b'\x88',
            'jA' : b'\x8c',
            'kA' : b'\x90',
            'lA' : b'\x94',
            'mA' : b'\x98',
            'nA' : b'\x9c',
            'oA' : b'\xa0',
            'pA' : b'\xa4',
            'qA' : b'\xa8',
            'rA' : b'\xac',
            'sA' : b'\xb0',
            'tA' : b'\xb4',
            'uA' : b'\xb8',
            'vA' : b'\xbc',
            'wA' : b'\xc0',
            'xA' : b'\xc4',
            'yA' : b'\xc8',
            'zA' : b'\xcc',
            '0A' : b'\xd0',
            '1A' : b'\xd4',
            '2A' : b'\xd8',
            '3A' : b'\xdc',
            '4A' : b'\xe0',
            '5A' : b'\xe4',
            '6A' : b'\xe8',
            '7A' : b'\xec',
            '8A' : b'\xf0',
            '9A' : b'\xf4',
            '+A' : b'\xf8',
            '/A' : b'\xfc',
        }
        for (valid_input, expected) in valid_inputs.items():
            with self.subTest(valid_input=valid_input):
                actual = util.base64.decode(valid_input)
                self.assertEqual(expected, actual)

    def test_invalid_decode(self):
        invalid_inputs = {
            'a': 'Invalid trailing single character provided for input: [base64_str[0:0]] + [a] + []',
            'aB': 'Invalid final trailing character provided for input: [base64_str[0:0]] + [aB] + [] (Final char must be [AQgw])',
            'aaB': 'Invalid final trailing character provided for input: [base64_str[0:0]] + [aaB] + [] (Final char must be [AEIMQUYcgkosw048])',
            '==': 'Invalid padding provided for input: [base64_str[0:0]] + [] + [==]',
            'AAA==': 'Invalid padding provided for input: [base64_str[0:0]] + [AAA] + [==]',
        }
        for (invalid_input, message) in invalid_inputs.items():
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(Base64Exception) as context_manager:
                    res = util.base64.decode(invalid_input)
                exception = context_manager.exception
                self.assertEqual(message, str(exception))

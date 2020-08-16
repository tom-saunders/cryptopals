import re

import bidict
import bitstring

class Base64Exception(Exception):
    def __init__(self, *args, **kwargs):
        super(Base64Exception, self).__init__(*args, **kwargs)

_base64_map = bidict.bidict({
    'A': '000000',
    'B': '000001',
    'C': '000010',
    'D': '000011',
    'E': '000100',
    'F': '000101',
    'G': '000110',
    'H': '000111',
    'I': '001000',
    'J': '001001',
    'K': '001010',
    'L': '001011',
    'M': '001100',
    'N': '001101',
    'O': '001110',
    'P': '001111',
    'Q': '010000',
    'R': '010001',
    'S': '010010',
    'T': '010011',
    'U': '010100',
    'V': '010101',
    'W': '010110',
    'X': '010111',
    'Y': '011000',
    'Z': '011001',
    'a': '011010',
    'b': '011011',
    'c': '011100',
    'd': '011101',
    'e': '011110',
    'f': '011111',
    'g': '100000',
    'h': '100001',
    'i': '100010',
    'j': '100011',
    'k': '100100',
    'l': '100101',
    'm': '100110',
    'n': '100111',
    'o': '101000',
    'p': '101001',
    'q': '101010',
    'r': '101011',
    's': '101100',
    't': '101101',
    'u': '101110',
    'v': '101111',
    'w': '110000',
    'x': '110001',
    'y': '110010',
    'z': '110011',
    '0': '110100',
    '1': '110101',
    '2': '110110',
    '3': '110111',
    '4': '111000',
    '5': '111001',
    '6': '111010',
    '7': '111011',
    '8': '111100',
    '9': '111101',
    '+': '111110',
    '/': '111111',
})

def _base64_char_to_bits(base64_char):
    if len(base64_char) != 1:
        raise Base64Exception('Can only convert one base64 char at a time')
    lookup = _base64_map.get(base64_char, None)
    if lookup:
        return bitstring.Bits(bin = lookup)
    else:
        raise Base64Exception('Invalid input: [{}] is not a base64 char'.format(chr(base64_char)))

def _base64_bits_to_char(base64_bits):
    bits = base64_bits.bin
    if len(bits) != 6:
        raise Base64Exception('Must convert six bits at a time')
    lookup = _base64_map.inverse.get(bits, None)
    if lookup:
        return lookup
    else:
        raise Base64Exception('Failed to convert input [{}] bits to base64 char'.format(base64_bits))

def _encode_3byte_to_4char(input_bytes):
    chars = ''
    if len(input_bytes) > 3:
        raise Base64Exception('Can only encode three bytes at a time')
    elif len(input_bytes) == 0:
        raise Base64Exception('Cannot encode empty bytes')

    provided_bits = len(input_bytes) * 8
    converting_bits = int(int(provided_bits + 5) / 6) * 6
    bitstr = bitstring.Bits(bytes = input_bytes, length = provided_bits) + bitstring.Bits(bin = '0000')
    for idx in range(0, converting_bits, 6):
        new_char = _base64_bits_to_char(bitstr[idx:idx + 6])
        chars += new_char
    chars += '=='
    return chars[0:4]

def _decode_4char_to_3byte(input_chars):
    if len(input_chars) > 4:
        raise Base64Exception('Can only decode input four chars at a time')
    depadded_input = input_chars.replace('=', '')
    if len(depadded_input) < 2:
        raise Base64Exception('Must have at least two non-padding characters to decode')

    provided_bits = len(depadded_input) * 6
    required_bits = int(int(provided_bits) / 8) * 8

    bits = _base64_char_to_bits(depadded_input[0])
    bits += _base64_char_to_bits(depadded_input[1])
    if len(depadded_input) >= 3:
        bits += _base64_char_to_bits(depadded_input[2])
    if len(depadded_input) == 4:
        bits += _base64_char_to_bits(depadded_input[3])
    decoded_bytes = bits[0:required_bits].tobytes()
    return decoded_bytes

_base64_pattern = re.compile(r'^(?:(([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{0,3}))(={0,2}))?$')
_base64_2char_trail = re.compile(r'[A-Za-z0-9+/][AQgw]')
_base64_3char_trail = re.compile(r'[A-Za-z0-9+/]{2}([AEIMQUYcgkosw048])')

def _decode(base64_str, assume_padding = False):
    decoded = b''

    match = _base64_pattern.match(base64_str)
    if not match:
        raise Base64Exception('Malformed base64 string: [{}]'.format(base64_str))
    base64_value = match.group(1)
    base64_pretrail = match.group(2)
    if not base64_pretrail:
        base64_pretrail = ''
    base64_trail = match.group(3)
    if not base64_trail:
        base64_trail = ''
    base64_padding = match.group(4)
    if not base64_padding:
        base64_padding = ''

    if len(base64_padding) == 1:
        if len(base64_trail) != 3:
            raise Base64Exception('Invalid padding provided for input: [base64_str[0:{}]] + [{}] + [{}]'.format(len(base64_pretrail), base64_trail, base64_padding))
    elif len(base64_padding) == 2:
        if len(base64_trail) != 2:
            raise Base64Exception('Invalid padding provided for input: [base64_str[0:{}]] + [{}] + [{}]'.format(len(base64_pretrail), base64_trail, base64_padding))

    if len(base64_trail) == 1:
            raise Base64Exception('Invalid trailing single character provided for input: [base64_str[0:{}]] + [{}] + [{}]'.format(len(base64_pretrail), base64_trail, base64_padding))

    if len(base64_trail) == 2:
        trail_match = _base64_2char_trail.match(base64_trail)
        if not trail_match:
            raise Base64Exception('Invalid final trailing character provided for input: [base64_str[0:{}]] + [{}] + [{}] (Final char must be [AQgw])'.format(len(base64_pretrail), base64_trail, base64_padding))
    elif len(base64_trail) == 3:
        trail_match = _base64_3char_trail.match(base64_trail)
        if not trail_match:
            raise Base64Exception('Invalid final trailing character provided for input: [base64_str[0:{}]] + [{}] + [{}] (Final char must be [AEIMQUYcgkosw048])'.format(len(base64_pretrail), base64_trail, base64_padding))

    for idx in range(0, len(base64_str), 4):
        dec = _decode_4char_to_3byte(base64_str[idx:idx+4])
        decoded += dec

    return decoded

def _encode(byte_str):
    encoded = ''
    for idx in range(0, len(byte_str), 3):
        enc = _encode_3byte_to_4char(byte_str[idx:idx+3])
        encoded += enc
    return encoded

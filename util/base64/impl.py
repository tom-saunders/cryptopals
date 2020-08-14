import bidict
import bitstring

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

    #if len(base64_char) != 1:
    #    raise Exception('Can only convert one char at a time')
    lookup = _base64_map.get(base64_char, None)
    if lookup:
        return bitstring.Bits(bin = lookup)
    else:
        raise Exception('Cannot convert input [{}] as a base64 char to bits'.format(chr(base64_char)))

def _base64_bits_to_char(base64_bits):
    bits = base64_bits.bin
    if len(bits) != 6:
        raise Exception('Can only convert six bits at a time')
    lookup = _base64_map.inverse.get(bits, None)
    if lookup:
        return lookup
    else:
        raise Exception('Cannot convert input [{}] as base64 bits to char'.format(base64_bits))

def _encode_3byte_to_4char(input_bytes, include_padding = True):
    chars = ''
    if len(input_bytes) > 3:
        raise Exception('Can only encode input three bytes at a time')
    elif len(input_bytes) == 3:
        bitstr = bitstring.Bits(bytes = input_bytes, length = 24)
        chars += _base64_bits_to_char(bitstr[0:6])
        chars += _base64_bits_to_char(bitstr[6:12])
        chars += _base64_bits_to_char(bitstr[12:18])
        chars += _base64_bits_to_char(bitstr[18:24])
    elif len(input_bytes) == 2:
        bitstr = bitstring.Bits(bytes=  input_bytes, length = 16) + bitstring.Bits(bin = '00')
        chars += _base64_bits_to_char(bitstr[0:6])
        chars += _base64_bits_to_char(bitstr[6:12])
        chars += _base64_bits_to_char(bitstr[12:18])
        if include_padding:
            chars += '='
    elif len(input_bytes) == 1:
        bitstr = bitstring.Bits(bytes = input_bytes, length = 8) + bitstring.Bits(bin = '0000')
        chars += _base64_bits_to_char(bitstr[0:6])
        chars += _base64_bits_to_char(bitstr[6:12])
        if include_padding:
            chars += '=='
    else:
        # been passed an empty byte array?
        pass
    return chars

def _decode_4char_to_3byte(input_chars):
    if len(input_chars) > 4:
        raise Exception('Can only decode input four chars at a time')
    depadded_input = input_chars.replace('=', '')
    if len(depadded_input) < 2:
        raise Exception('Must have at least two non-padding characters to decode')
    bits = _base64_char_to_bits(depadded_input[0])
    bits += _base64_char_to_bits(depadded_input[1])
    if len(depadded_input) == 2:
        decoded_bytes = bits[0:7].tobytes()
    if len(depadded_input) == 3:
        bits += _base64_char_to_bits(depadded_input[2])
        decoded_bytes = bits[0:15].tobytes()
    if len(depadded_input) == 4:
        bits += _base64_char_to_bits(depadded_input[2])
        bits += _base64_char_to_bits(depadded_input[3])
        decoded_bytes = bits.tobytes()
    return decoded_bytes

def decode(base64_chars, assume_padding = False):
    decoded = b''
    for idx in range(0, len(base64_chars), 4):
        dec = _decode_4char_to_3byte(base64_chars[idx:idx+4])
        decoded += dec

    return decoded

def encode(byte_str, include_padding = True):
    encoded = ''
    for idx in range(0, len(byte_str), 3):
        enc = _encode_3byte_to_4char(byte_str[idx:idx+3])
        encoded += enc
    return encoded

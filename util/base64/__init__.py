import util.base64.impl as impl

decode = impl._decode
encode = impl._encode

def decode_to_hex(base64_str):
    byte_str = decode(base64_str)
    hex_str = byte_str.hex()
    return hex_str

def encode_from_hex(hex_str):
    byte_str = bytes.fromhex(hex_str)
    return encode(byte_str)

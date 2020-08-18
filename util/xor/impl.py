class XorException(Exception):
    def __init__(self, *args, **kwargs):
        super(XorException, self).__init__(*args, **kwargs)

def _fixed(left_bytes, right_bytes):
    left_len = len(left_bytes)
    right_len = len(right_bytes)

    if left_len != right_len:
        raise XorException('Mismatched input lengths: l[{}] r[{}]'.format(left_len, right_len))

    result_bytes = b''

    for (left_byte, right_byte) in zip(left_bytes, right_bytes):
        result_byte = left_byte ^ right_byte
        result_bytes += bytes([result_byte])

    return result_bytes

def _repeated_bytes(byte_str, key_str):
    req_len = len(byte_str)
    key_len = len(key_str)

    if key_len == 0:
        raise XorException('Cannot xor with repeated empty string')
    elif req_len <= key_len:
        return _fixed(byte_str, key_str[0:req_len])
    else:
        req_copies = int((req_len + key_len - 1) / key_len)
        repeated_key = key_str * req_copies
        return _fixed(byte_str, repeated_key[0:req_len])


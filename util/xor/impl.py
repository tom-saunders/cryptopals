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

import base64


def encode(key):
    byte = key.encode('utf-8')     # turn password into bytes
    enc = list(base64.b64encode(byte))  # store base 64 encoding in a list

    return enc


def decode(enc):
    enc = ''.join(chr(b) for b in enc).encode('utf-8')
    dec = base64.b64decode(enc)
    key = str(dec, 'utf-8')

    return key

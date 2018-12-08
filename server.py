import socket
s = socket.socket()

host=socket.gethostname()
port=12457
s.bind((host,port))
s.listen(5)
while True:
    c,addr=s.accept()
    print("Got connection from home",addr)
    c.send("alarm")
    c.close()


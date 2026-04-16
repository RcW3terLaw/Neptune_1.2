import socks

ONION = "oabtt5q4uqwsienlw55r7rcdveeudjdixpm4fsq6zlzz262gvtxqnfyd.onion"
PORT = 1234

s = socks.socksocket()
s.set_proxy(socks.SOCKS5, "127.0.0.1", 9052) 

print("Connexion à", ONION)

s.connect((ONION, PORT))
print("Connecté !")

while True:    
    data = s.recv(1024)
    print(data.decode())
    s.send(f"[CLIENT] Correctly recieve {data.decode()}".encode())
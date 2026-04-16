import socks

ONION = "oabtt5q4uqwsienlw55r7rcdveeudjdixpm4fsq6zlzz262gvtxqnfyd.onion"
PORT = 1234

s = socks.socksocket()
s.set_proxy(socks.SOCKS5, "127.0.0.1", 9052)
s.settimeout(10)

print("Connexion à", ONION)

s.connect((ONION, PORT))
print("Connecté !")

while True:
    try:
        data = s.recv(1024)

        if not data:
            break

        msg = data.decode()
        print(msg)

        s.send(f"[CLIENT] received: {msg}".encode())

    except Exception as e:
        print("Erreur:", e)
        break
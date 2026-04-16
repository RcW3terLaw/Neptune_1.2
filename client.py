import socks
import subprocess
import time

ONION = "5p7php7kszebdfgghrxkp6ivcpqdmvhhc7lpvb2c7v72vcwh6yy5umyd.onion"
PORT = 1234

tor = subprocess.Popen(
    [".\\payload\\TorClient\\tor.exe", "-f", ".\\payload\\TorClient\\torrc"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

booted = False

for line in tor.stdout:
    print("[TOR]", line.strip())

    if "Bootstrapped 100%" in line:
        booted = True
        break

if booted:
    time.sleep(1)

    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050) 
    s.settimeout(10)

    print("[CLIENT]Connexion à :", ONION)

    s.connect((ONION, PORT))
    print("[CLIENT]Connecté")

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

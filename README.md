# ARPocalypse 

ARPocalypse es una herramienta de seguridad que implementa la técnica de ARP spoofing para bloquear la conexión a Internet de un dispositivo en una red local. Está diseñado con fines educativos y de prueba en entornos controlados.

## Características 
- Bloqueo de conexión mediante envío de paquetes ARP falsos.
- Restauración automática de la tabla ARP al detener el script.
- Validación de direcciones IP para evitar errores.
- Compatible con sistemas Linux.

## Requisitos 
- Python 3.x
- Scapy (`pip install scapy`)
- Permisos de superusuario (root)

## Instalación 🚀
1. Clona el repositorio:
   ```bash
   git clone https://github.com/retr0-bit011/ARPocalypse.git
   cd ARPocalypse
   ```
2. Instala dependencias
   ```bash
   pip install scapy
   ```
3. Ejecuta el script
   ```bash
   python3 ARPocalypse.py
   ```
## Ejemplo de Uso
Ejecuta el script como superusuario.
```bash
sudo python3 ARPocalypse.py
Ingrese la IP del router: 192.168.1.1
Ingrese la IP de la víctima: 192.168.1.100
[+] Bloqueando a 192.168.1.100 (router: 192.168.1.1, MAC real: 00:1A:2B:3C:4D:5E)
[!] Ataque detenido. Restaurando conexión...
[✔] Conexión restaurada con éxito.
```
## Actualización
1. Se mejoró el escaneo.
2. Detección del router automaticamente.
3. Envio de paquetes con mayor frecuencia.
4. Selección de IP o ingreso manualmente.

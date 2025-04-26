import nmap
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
import os 

def scan_services(network):
    nm = nmap.PortScanner()

    nm.scan(hosts=network, arguments="-sV")
    
    network_data = {}

    for host in nm.all_hosts():
        if nm[host].state() == "up":

            network_data[host] = {}
            for proto in nm[host].all_protocols():
                network_data[host][proto] = {}
                ports = nm[host][proto].keys()

                for port in ports:
                    service = nm[host][proto][port].get("name", "")
                    producto = nm[host][proto][port].get("product", "")
                    version = nm[host][proto][port].get("version", "")

                    network_data[host][proto][port] = {
                        "service": service,
                        "product": producto,
                        "version": version
                    }
    return network_data


def print_services(services):
    console = Console()
    table = Table(title="Escaneo de servicios")

    table.add_column("Host", style="cyan", no_wrap=True)
    table.add_column("Protocolo", style="magenta")
    table.add_column("Puerto", style="blue")
    table.add_column("Servicio", style="red")
    table.add_column("Nombre", style="yellow")
    table.add_column("Version", style="green")

    for host, protocols in services.items():
        for proto, ports  in protocols.items():
            for port, info in ports.items():
                table.add_row(
                    host, proto, str(port), info.get("service", ""), info.get("producto", ""), info.get("version", "")
                )
    console.print(table)



if __name__ == "__main__":
    load_dotenv()
    network = os.getenv("TARGET_NETWORK")
    print(network)
    services = scan_services(network)
    print_services(services)

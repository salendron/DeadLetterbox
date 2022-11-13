import network
import rp2

def start_ap():
    rp2.country('AT')
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='Dead Letter Box', password='12345678')
    ap.active(True)

    netConfig = ap.ifconfig()
    print('IPv4-Adresse:', netConfig[0], '/', netConfig[1])
    print('Standard-Gateway:', netConfig[2])
    print('DNS-Server:', netConfig[3])

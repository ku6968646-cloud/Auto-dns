import socket
import time
import threading

# အဓိက DNS ဆာဗာများစာရင်း (IP နှင့် Port)
DNS_SERVERS = [
    {"name": "Cloudflare", "ip": "1.1.1.1", "port": 53, "ping": 999},
    {"name": "Google", "ip": "8.8.8.8", "port": 53, "ping": 999},
    {"name": "Quad9", "ip": "9.9.9.9", "port": 53, "ping": 999},
    {"name": "OpenDNS", "ip": "208.67.222.222", "port": 53, "ping": 999}
]

ACTIVE_DNS = DNS_SERVERS[0]

# DNS တစ်ခုချင်းစီ၏ Latency (Ping) ကို တိုင်းတာသည့် ဖန်ရှင်
def measure_ping(dns):
    start_time = time.time()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((dns["ip"], dns["port"]))
        s.close()
        latency = (time.time() - start_time) * 1000
        return round(latency, 2)
    except:
        return 999.0

# နောက်ကွယ်တွင် အမြဲတမ်း Ping တိုင်းပြီး အကောင်းဆုံးလိုင်းသို့ Auto-Switch လုပ်မည့် Background Worker
def background_dns_monitor():
    global ACTIVE_DNS
    while True:
        best_dns = ACTIVE_DNS
        min_ping = 999
        
        for dns in DNS_SERVERS:
            p = measure_ping(dns)
            dns["ping"] = p
            print(f"[{dns['name']}] Ping: {p} ms")
            if p < min_ping:
                min_ping = p
                best_dns = dns
                
        ACTIVE_DNS = best_dns
        print(f"--> [Auto-Switched] လက်ရှိအကောင်းဆုံး DNS: {ACTIVE_DNS['name']} ({ACTIVE_DNS['ping']}ms)\n")
        time.sleep(15) # ဘက်ထရီသက်သာစေရန် ၁၅ စက္ကန့်တစ်ကြိမ် သတ်မှတ်ထားသည်

# Local DNS Proxy Server (ဖုန်းအတွင်းမှ DNS တောင်းဆိုမှုများကို လက်ခံရန်)
def start_dns_proxy():
    local_ip = "127.0.0.1"
    local_port = 5353
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Port ချက်ချင်းပြန်လွတ်စေရန် (Address already in use error ကာကွယ်ရန်)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.bind((local_ip, local_port))
    print(f"[*] DNS Proxy Server ကို {local_ip}:{local_port} တွင် စတင်လိုက်ပါပြီ...")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            forward_sock.settimeout(2.0)
            forward_sock.sendto(data, (ACTIVE_DNS["ip"], ACTIVE_DNS["port"]))
            
            response, _ = forward_sock.recvfrom(512)
            sock.sendto(response, addr)
            forward_sock.close()
        except Exception as e:
            pass

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=background_dns_monitor, daemon=True)
    monitor_thread.start()
    
    start_dns_proxy()


from dataclasses import dataclass, asdict # dataclass'ı dict'e çevirmek için
import json

#------------------------------------------------------
# Bölüm 1
#------------------------------------------------------
print("------------------------------------------------------")

sirket_adi: str = "SecFlowX"
kurulus_yili: int = 2003
aktif_musteri_sayisi: int = 47
ortalama_risk_skoru: float = 6.8
kvkk_uyumlu_mu: bool = True

print("Şirket adı : " + sirket_adi)
print("Kurluş yılı : " + str(kurulus_yili))
print("Aktif müşteri sayısı : " + str(aktif_musteri_sayisi))
print("Ortalama risk skoru : " + str(ortalama_risk_skoru))
print("KVKK uyumlu mu : " + "Evet" if kvkk_uyumlu_mu else "Hayır")
print("------------------------------------------------------")

#------------------------------------------------------
# Bölüm 2
#------------------------------------------------------
desteklenen_portlar: list[int] = [22, 80, 443, 3306, 8080]
print(desteklenen_portlar)

desteklenen_portlar.append(8443)
print(desteklenen_portlar)

kritik_portlar: set[int] = {22, 443, 22, 3306}
print(kritik_portlar)

# tuple kullanmamızın sebebi bu değerler değiştirilemez sabit olması gerektiği için
sabit_konfigirasyon: tuple[str,str] = ("v1.0","production")
print(sabit_konfigirasyon)

host_envanteri: dict[str, dict[str, str | float]] = {
    "web-01": {"ip": "192.168.1.10", "durum": "aktif", "risk_skoru": 7.2},
    "db-01": {"ip": "192.168.1.20", "durum": "aktif", "risk_skoru": 9.1},
    "test-01": {"ip": "192.168.1.30", "durum": "pasif", "risk_skoru": 2.5},
}

for key, value in host_envanteri.items():
    print(f"{key} -> IP : {value['ip']}, Durum : {value['durum']}, Risk : {value['risk_skoru']}")

print("------------------------------------------------------")

#------------------------------------------------------
# Bölüm 3
#------------------------------------------------------
def risk_seviyesi_belirle(skor: float) -> str:
    if skor >= 7.0:
        return "Yüksek"
    elif skor > 4.0 and skor <= 6.9:
        return "Orta"
    else:
        return "Düşük"

def host_durumu_metni(durum: str) -> str:
    return "🟢 Çalışıyor" if durum == "aktif" else "🔴 Kapalı"

for key, value in host_envanteri.items():
    print(f"{key} -> {host_durumu_metni(str(value['durum']))}, Risk Seviyesi: {risk_seviyesi_belirle(float(value['risk_skoru']))}")

print("------------------------------------------------------") 

#------------------------------------------------------
# Bölüm 4
#------------------------------------------------------
@dataclass
class Host:
    isim: str
    ip: str
    durum: str
    risk_skoru: float

host_listesi: list[Host] = []

for key, value in host_envanteri.items():
    host = Host(
        isim = key,
        ip = str(value["ip"]),
        durum = str(value["durum"]),
        risk_skoru = float(value["risk_skoru"])
    )
    host_listesi.append(host)

for rec in host_listesi:
    print("Host: " + rec.isim)
    print("Risk Skoru: " + str(rec.risk_skoru))

# dataclass tip güvenliği sağlıyor ve sabit yapılı olduğu için tekrar kullanılabilir.

print("------------------------------------------------------") 

#------------------------------------------------------
# Bölüm 5
#------------------------------------------------------
yuksek_riskli_hostlar = [host.isim for host in host_listesi if host.risk_skoru >= 7.0]
print(yuksek_riskli_hostlar)

isim_skor = [f"{host.isim} : {host.risk_skoru}" for host in host_listesi if host.risk_skoru >= 7.0]
print(isim_skor)

print("------------------------------------------------------") 

#------------------------------------------------------
# Bölüm 6
#------------------------------------------------------
def port_kontrol(port: int) -> str:
    if 1 <= port <= 65535: # bu kallnım beyween gibi and olmadan kullanılıyor.
        return f"Port {port} geçerli"
    else:
        raise ValueError (f"{port} numaralı port 1 ile 65535 arasında olmalıdır.")

port_list = [22, 243, 99999, -5, 8080]

for port in port_list:
    try:
        print(port_kontrol(port))
    except ValueError as e:
        print(f"Hata: {e}")
    finally:
        print("--- kontrol tamamlandı ---")
        
print("------------------------------------------------------")

#------------------------------------------------------
# Bölüm 7
#------------------------------------------------------
veri = [asdict(host) for host in host_listesi]

with open("host_envanteri.json", "w") as f:
    json.dump(veri,f)

try:
    with open("host_envanteri.json", "r") as f:
        veri = json.load(f)
        print(veri)
        
except FileNotFoundError:
    print("Dosya bulunamadı.")

print("------------------------------------------------------")

#------------------------------------------------------
# Bonus
#------------------------------------------------------
def port_araligi_say(baslangic: int, bitis: int) -> int:
    if baslangic > bitis:
        return 0
    else:
        print(bitis - baslangic)
        return 1 + port_araligi_say(baslangic + 1, bitis)
    
print(port_araligi_say(5,10))
print("------------------------------------------------------")
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

kayitli_hostlar = {
    "192.168.1.1": "router",
    "10.0.0.1": "firewall",
    "172.16.0.1": "switch"
}

def ip_dogrula(ip_adresi: str) -> str:
    parcalar = ip_adresi.split(".") 
    # split(".") gelen stringi içinde yazan karakter nezlinde bölüp arada kalan değerler ile bir liste oluşturuyor.
    # len -> sadece karakter saymaz değişken liste ise liste içindeki elemanlarıda sayar veya dictse dict içindeki keyleride sayar
    # all for daki her p için kontrol yapıyor, isdigit() -> sayımı
    if len(parcalar) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parcalar):
        raise HTTPException(status_code=400, detail="Geçersiz IP adresi")
    return ip_adresi

#------------------------------------------------------------------------------------
# main.py sqldeki paket gibi düşün
# host_sorgula, tara bizim prosedür/fonskiyonlarımız
# classlar sonucu gösterme stilimiz
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# GET -> veri okuma(select ile veri okuma)
#------------------------------------------------------------------------------------
class HostSonuc(BaseModel):
    sorgu: str
    durum: str
    port_sayisi: int | None = None # PL/SQL de default NULL gibi
    protokol: str | None = None
    cihaz: str | None = None

@app.get("/")
def root():
    return {"mesaj": "SecFlowX API çalışıyor!"}

@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str = Depends(ip_dogrula), detay: bool = False) -> HostSonuc:    
    if ip_adresi not in kayitli_hostlar:
        raise HTTPException(status_code=404, detail="Host bulunamadı")
      
    cihaz = kayitli_hostlar[ip_adresi]
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if ip_adresi in ozel_ipler else "dış ağ"

    if detay:
        return HostSonuc(sorgu=ip_adresi, durum=durum, port_sayisi=1024, protokol="TCP")
    
    return HostSonuc(sorgu=ip_adresi, durum=durum, cihaz=cihaz)

#------------------------------------------------------------------------------------
# POST -> veri işleyerek okuma (fonksiyon sonucu gelen veriyi okuma)
#------------------------------------------------------------------------------------

class TaramaIstegi(BaseModel):
    ip_adresi: str
    port: int = 80
    protokol: str = "TCP"

@app.post("/tara")
def tara(istek: TaramaIstegi) -> HostSonuc:
    ip_dogrula(istek.ip_adresi)
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if istek.ip_adresi in ozel_ipler else "dış ağ"
    
    return HostSonuc(sorgu=istek.ip_adresi, durum=durum, port_sayisi=istek.port, protokol=istek.protokol)
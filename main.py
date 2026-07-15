from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from fastapi.security import OAuth2PasswordBearer
import httpx

app = FastAPI()

GIZLI_ANAHTAR = "secflowx-super-gizli-anahtar-2024"
ALGORITMA = "HS256"
TOKEN_SURESI = 30  # dakika

# OAuth2PasswordBearer — FastAPI'ye "bu endpoint token bekliyor, token /giris'ten alınır" diyor.
# tokenUrl="/giris" — sadece Swagger'a "token almak için buraya git" demek. Yönlendirme yapıyor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/giris")

kayitli_hostlar = {
    "192.168.1.1": "router",
    "10.0.0.1": "firewall",
    "172.16.0.1": "switch"
}
sahte_kullanicilar = {
    "caner": {
        "kullanici_adi": "caner",
        "sifre_hash": bcrypt.hashpw("sifre123".encode(), bcrypt.gensalt()).decode()
    }
}

def token_olustur(veri: dict) -> str:
    payload = veri.copy()
    bitis = datetime.utcnow() + timedelta(minutes=TOKEN_SURESI)
    payload.update({"exp": bitis})
    return jwt.encode(payload, GIZLI_ANAHTAR, algorithm=ALGORITMA)

def token_dogrula(token: str) -> str:
    try:
        payload = jwt.decode(token, GIZLI_ANAHTAR, algorithms=[ALGORITMA])
        kullanici = payload.get("sub")
        if kullanici is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        return kullanici
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")

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
def host_sorgula(ip_adresi: str = Depends(ip_dogrula), detay: bool = False, token: str = Depends(oauth2_scheme)) -> HostSonuc:    
    kullanici = token_dogrula(token)
    
    if ip_adresi not in kayitli_hostlar:
        raise HTTPException(status_code=404, detail="Host bulunamadı")
      
    cihaz = kayitli_hostlar[ip_adresi]
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if ip_adresi in ozel_ipler else "dış ağ"

    if detay:
        return HostSonuc(sorgu=ip_adresi, durum=durum, port_sayisi=1024, protokol="TCP")
    
    return HostSonuc(sorgu=ip_adresi, durum=durum, cihaz=cihaz)

@app.get("/dis-servis/{ip_adresi}")
async def dis_servis_sorgula(ip_adresi: str = Depends(ip_dogrula)):
    async with httpx.AsyncClient() as client:
        yanit = await client.get(f"http://ip-api.com/json/{ip_adresi}")
    return {"ip": ip_adresi, "dis_servis_yaniti": yanit.json()}

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

class GirisIstegi(BaseModel):
    kullanici_adi: str
    sifre: str
    
@app.post("/giris")
def giris(istek: GirisIstegi):
    kullanici = sahte_kullanicilar.get(istek.kullanici_adi)
    if not kullanici:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
    if not bcrypt.checkpw(istek.sifre.encode(), kullanici["sifre_hash"].encode()):
        raise HTTPException(status_code=401, detail="Yanlış şifre")
    token = token_olustur({"sub": istek.kullanici_adi})
    return {"access_token": token, "token_type": "bearer"}
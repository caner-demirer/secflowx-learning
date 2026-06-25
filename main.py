from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HostSonuc(BaseModel):
    sorgu: str
    durum: str
    port_sayisi: int | None = None # PL/SQL de default NULL gibi
    protokol: str | None = None

@app.get("/")
def root():
    return {"mesaj": "SecFlowX API çalışıyor!"}

@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str, detay: bool = False) -> HostSonuc:
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if ip_adresi in ozel_ipler else "dış ağ"

    if detay:
        return HostSonuc(sorgu=ip_adresi, durum=durum, port_sayisi=1024, protokol="TCP")
    
    return HostSonuc(sorgu=ip_adresi, durum=durum)
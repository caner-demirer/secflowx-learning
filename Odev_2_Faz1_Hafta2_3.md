# 📝 Ödev 3 — Faz 1 / Hafta 2 + Hafta 3: FastAPI + PostgreSQL

> Bu ödev hafta 2 (FastAPI, JWT, httpx) ve hafta 3 (SQLAlchemy, PostgreSQL) konularını birleştiriyor.
> Cihaz envanterini artık veritabanında tutacaksın.

**Dosyalar:**
- `odev3_db.py` → veritabanı modeli ve bağlantı
- `odev3.py` → FastAPI uygulaması

**Çalıştırma:** `uvicorn odev3:app --reload`

**Veritabanı:** `odev3` database'i (zaten oluşturduk)

---

## Bölüm 1 — Veritabanı Modeli (Kolay)

`odev3_db.py` dosyası oluştur. İçine şunları yaz:

- `DATABASE_URL` → `odev3` database'ine bağlan (secflowx kullanıcısı ile)
- `engine`, `SessionLocal`, `Base` tanımla
- `Cihaz` adında SQLAlchemy modeli oluştur, şu alanlarla:
  - `id` → primary key
  - `ip_adresi` → String, unique
  - `cihaz_adi` → String
  - `tip` → String (örn: "router", "switch", "firewall")
  - `aktif` → Boolean, default True
  - `olusturma_tarihi` → DateTime, default şimdiki zaman

Dosyanın sonuna şunu ekle — tabloları otomatik oluştursun:
```python
Base.metadata.create_all(bind=engine)
```

---

## Bölüm 2 — FastAPI Kurulumu (Kolay)

`odev3.py` dosyası oluştur.

- Gerekli import'ları yap (`odev3_db.py`'dan da import et)
- `app = FastAPI()` ile başlat
- `get_db` dependency'sini yaz
- Başlangıç verisi olarak 3 cihaz ekleyen bir fonksiyon yaz ve uygulama başlarken çalıştır:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # uygulama başlarken çalışır
    db = SessionLocal()
    if db.query(Cihaz).count() == 0:
        baslangic_cihazlar = [
            Cihaz(ip_adresi="192.168.1.1", cihaz_adi="ana-router", tip="router"),
            Cihaz(ip_adresi="10.0.0.1", cihaz_adi="merkez-switch", tip="switch"),
            Cihaz(ip_adresi="172.16.0.1", cihaz_adi="cevre-firewall", tip="firewall"),
        ]
        db.add_all(baslangic_cihazlar)
        db.commit()
    db.close()
    yield

app = FastAPI(lifespan=lifespan)
```

`GET /` endpoint'i yaz — şunu döndürsün:
```json
{"mesaj": "Ağ Envanter API çalışıyor"}
```

---

## Bölüm 3 — Pydantic Response Modeli (Kolay)

`CihazResponse` adında bir Pydantic modeli oluştur — endpoint'lerin ne döndüreceğini tanımlar:

- `id: int`
- `ip_adresi: str`
- `cihaz_adi: str`
- `tip: str`
- `aktif: bool`

❓ **Düşünme sorusu (yorum satırı olarak cevapla):** SQLAlchemy modeli ile Pydantic modeli aynı alanları içeriyor — neden iki ayrı model kullanıyoruz?

---

## Bölüm 4 — GET Endpoint'leri (Orta)

**`GET /cihazlar`** — veritabanındaki tüm cihazları döndür.
- `tip` query parameter ekle — opsiyonel, verilirse sadece o tipteki cihazları döndür.

**`GET /cihaz/{ip_adresi}`** — tek cihaz getir.
- IP doğrulaması `Depends` ile yapılmalı
- Envanterde yoksa 404 döndür

Test:
```
GET /cihazlar              → hepsi
GET /cihazlar?tip=router   → sadece router'lar
GET /cihaz/192.168.1.1     → tek cihaz
GET /cihaz/abc             → 400
GET /cihaz/1.2.3.4         → 404
```

---

## Bölüm 5 — POST ve DELETE Endpoint'leri (Orta)

**`POST /cihaz`** — yeni cihaz ekle.
- Body'den `CihazResponse` değil, ayrı bir `CihazEkle` Pydantic modeli gelecek (`id` ve `olusturma_tarihi` olmadan)
- Aynı IP zaten varsa 400 döndür: `"Bu IP zaten kayıtlı"`
- Yoksa veritabanına ekle, eklenen cihazı döndür

**`DELETE /cihaz/{ip_adresi}`** — cihaz sil.
- IP doğrulaması `Depends` ile
- Envanterde yoksa 404
- Varsa sil, `{"mesaj": "Cihaz silindi"}` döndür

---

## Bölüm 6 — httpx ile OSINT (Orta)

**`GET /cihaz/{ip_adresi}/osint`** — `ip-api.com`'dan o IP hakkında bilgi çek.

- `async def` olmalı
- `httpx.AsyncClient` kullan
- IP doğrulaması `Depends` ile
- Envanterde yoksa 404
- Döndüreceğin response:
```json
{
  "ip": "192.168.1.1",
  "cihaz_bilgisi": { ... },
  "osint": { ... }
}
```
`cihaz_bilgisi` → veritabanından, `osint` → `ip-api.com`'dan

---

## Bölüm 7 — JWT Kimlik Doğrulama (Zor)

`POST /giris` endpoint'i yaz. En az bir kullanıcı tanımla (hafta 2'deki gibi).

Şu endpoint'leri JWT ile koru:
- `GET /cihaz/{ip_adresi}`
- `GET /cihaz/{ip_adresi}/osint`
- `POST /cihaz`
- `DELETE /cihaz/{ip_adresi}`

Terminal ile test et:
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/giris \
  -H "Content-Type: application/json" \
  -d '{"kullanici_adi": "...", "sifre": "..."}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

curl -X GET http://127.0.0.1:8000/cihaz/192.168.1.1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## ✅ Teslim Öncesi Kontrol Listesi

- [ ] `GET /` çalışıyor
- [ ] Uygulama başlarken 3 cihaz otomatik DB'ye ekleniyor
- [ ] `GET /cihazlar` tüm cihazları döndürüyor
- [ ] `GET /cihazlar?tip=router` sadece router'ları döndürüyor
- [ ] `GET /cihaz/{ip_adresi}` — geçersiz IP 400, olmayan IP 404, geçerli IP 200
- [ ] `POST /cihaz` — yeni cihaz ekliyor, aynı IP 400
- [ ] `DELETE /cihaz/{ip_adresi}` — cihaz siliyor, olmayan IP 404
- [ ] `GET /cihaz/{ip_adresi}/osint` — dış servis bilgisi geliyor
- [ ] Token olmadan korumalı endpoint'ler 401 döndürüyor
- [ ] Token ile korumalı endpoint'ler 200 döndürüyor

---

## 💡 Notlar

- `odev3_db.py` tamamen bağımsız — `database.py`'a dokunma
- Takıldığında önce 5-10 dakika kendi başına dene
- Hata mesajını oku, uvicorn terminalde ne diyorsa oradan başla
- Bitirince bana gönder, satır satır review yapalım 💪

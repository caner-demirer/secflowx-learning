# 📝 Ödev 2 — Faz 1 / Hafta 2: FastAPI

> Bu ödev, öğrendiğin tüm FastAPI konularını (path/query parameter, Pydantic, POST endpoint, HTTP hata kodları, dependency injection, JWT, httpx) **gerçekçi bir mini senaryo** üzerinden pekiştirmek için tasarlandı.

**Senaryo:** SecFlowX'in **Ağ Envanter API'si**'ni yazıyorsun — şirketteki ağ cihazlarını yönetecek, sorgulayacak ve dış servislerden bilgi çekecek bir API.

**Nasıl çalışacaksın:**
- Her bölümü sırayla yap, bir önceki bölümün kodunu bir sonrakinde kullanacaksın.
- Dosya adı: `odev2.py` — ama `uvicorn odev2:app --reload` ile çalıştıracaksın.
- Her bölümü yazdıktan sonra `/docs`'ta test et.
- Takılırsan, ne denediğini ve aldığın hatayı bana göster — birlikte çözeriz.

---

## Bölüm 1 — Proje Kurulumu (Kolay)

`secflowx-proje` klasöründe (venv aktifken) `odev2.py` dosyası oluştur.

Gerekli import'ları yap ve `app = FastAPI()` ile uygulamayı başlat.

`GET /` endpoint'i yaz — şunu döndürsün:
```json
{"mesaj": "Ağ Envanter API çalışıyor"}
```

`uvicorn odev2:app --reload` ile başlat, `/docs`'ta gör.

---

## Bölüm 2 — Pydantic Modeli (Kolay)

`Cihaz` adında bir Pydantic modeli oluştur, şu alanlarla:
- `ip_adresi: str`
- `cihaz_adi: str`
- `tip: str` — örn: `"router"`, `"switch"`, `"firewall"`
- `aktif: bool = True`

Ayrıca başlangıç verisi olarak şu global dict'i ekle:

```python
cihaz_envanteri: dict[str, Cihaz] = {
    "192.168.1.1": Cihaz(ip_adresi="192.168.1.1", cihaz_adi="ana-router", tip="router"),
    "10.0.0.1": Cihaz(ip_adresi="10.0.0.1", cihaz_adi="merkez-switch", tip="switch"),
    "172.16.0.1": Cihaz(ip_adresi="172.16.0.1", cihaz_adi="cevre-firewall", tip="firewall"),
}
```

❓ **Düşünme sorusu (yorum satırı olarak cevapla):** Neden dict'in value'su olarak düz string veya dict yerine `Cihaz` modeli kullandık?

---

## Bölüm 3 — GET Endpoint'leri (Orta)

**`GET /cihazlar`** — `cihaz_envanteri`'ndeki tüm cihazları liste olarak döndür.

**`GET /cihaz/{ip_adresi}`** — tek cihaz getir. IP envanterde yoksa 404 döndür.

`/docs`'ta her ikisini de test et.

---

## Bölüm 4 — IP Doğrulama ve Dependency Injection (Orta)

`ip_dogrula(ip_adresi: str) -> str` fonksiyonunu yaz — geçersiz IP'de 400 döndürsün.

`Depends` ile bunu `GET /cihaz/{ip_adresi}` endpoint'ine bağla.

`/docs`'ta `abc` ve `192.168.999.999` ile test et — 400 gelmeli.

---

## Bölüm 5 — POST Endpoint (Orta)

**`POST /cihaz`** — yeni cihaz ekle.

- Body'den `Cihaz` modeli gelecek
- Aynı IP zaten varsa 400 döndür: `"Bu IP zaten kayıtlı"`
- Yoksa `cihaz_envanteri`'ne ekle, eklenen cihazı döndür

`/docs`'ta yeni bir cihaz ekle, sonra `GET /cihazlar` ile listede göründüğünü doğrula.

---

## Bölüm 6 — Query Parameter (Orta)

`GET /cihazlar` endpoint'ine `tip` query parameter ekle — opsiyonel, default `None` olsun.

- `tip` verilmişse sadece o tipteki cihazları döndür
- Verilmemişse hepsini döndür

Test:
```
GET /cihazlar             → hepsi
GET /cihazlar?tip=router  → sadece router'lar
```

---

## Bölüm 7 — httpx ile OSINT (Zor)

**`GET /cihaz/{ip_adresi}/osint`** — `ip-api.com`'dan o IP hakkında bilgi çek.

- `async def` olmalı
- `httpx.AsyncClient` kullan
- IP doğrulaması `Depends` ile yapılmalı
- Döndüreceğin response:
```json
{
  "ip": "8.8.8.8",
  "cihaz_bilgisi": { ... },
  "osint": { ... }
}
```
`cihaz_bilgisi` → `cihaz_envanteri`'nden, `osint` → `ip-api.com`'dan gelecek. IP envanterde yoksa 404 döndür.

---

## Bölüm 8 — JWT Kimlik Doğrulama (Zor)

`POST /giris` endpoint'i yaz. En az bir kullanıcı tanımla.

`GET /cihaz/{ip_adresi}` ve `GET /cihaz/{ip_adresi}/osint` endpoint'lerini JWT ile koru.

Token olmadan istek atınca 401 gelmeli, token ile 200 gelmeli.

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
- [ ] `GET /cihazlar` tüm cihazları döndürüyor
- [ ] `GET /cihazlar?tip=router` sadece router'ları döndürüyor
- [ ] `GET /cihaz/{ip_adresi}` — geçersiz IP 400, olmayan IP 404, geçerli IP 200
- [ ] `POST /cihaz` — yeni cihaz ekliyor, aynı IP 400
- [ ] `GET /cihaz/{ip_adresi}/osint` — dış servis bilgisi geliyor
- [ ] Token olmadan korumalı endpoint'ler 401 döndürüyor
- [ ] Token ile korumalı endpoint'ler 200 döndürüyor

---

## 💡 Notlar

- Takıldığın yerde önce **kendi başına 5-10 dakika** denemeni öneririm.
- Hata mesajlarını **okumaya çalış** — uvicorn terminal'de ne diyorsa oradan başla.
- Bölümleri sırayla yap, atlamaya çalışma.
- Bitirince bana gönder, satır satır review yapayım. 😊

**Kolay gelsin! 💪**

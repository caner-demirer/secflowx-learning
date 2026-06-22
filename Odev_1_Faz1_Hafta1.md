# 📝 Ödev 1 — Faz 1 / Hafta 1: Python Temelleri

> Bu ödev, öğrendiğin tüm konuları (type hints, koleksiyonlar, fonksiyonlar, exception handling, dataclass, comprehension, context manager) **gerçekçi bir mini senaryo** üzerinden pekiştirmek için tasarlandı.

**Senaryo:** Küçük bir "host envanteri" sistemi yazıyorsun — SecFlowX'in çekirdek mantığının minik bir versiyonu.

**Nasıl çalışacaksın:**
- Her bölümü sırayla yap, bir önceki bölümün kodunu bir sonrakinde kullanacaksın.
- Dosya adı: `odev1.py` (proje klasörünün içinde, `venv` aktifken).
- Her bölümü yazdıktan sonra **çalıştır**, sonra `ruff check odev1.py` ve `mypy odev1.py` ile kontrol et.
- Takılırsan, ne denediğini ve aldığın hatayı bana göster — birlikte çözeriz.

---

## Bölüm 1 — Değişkenler ve Tipler (Kolay)

Aşağıdaki değişkenleri **type hint** kullanarak tanımla:

- `sirket_adi` → "SecFlowX" değerinde bir string
- `kurulus_yili` → 2023 değerinde bir int
- `aktif_musteri_sayisi` → 47 değerinde bir int
- `ortalama_risk_skoru` → 6.8 değerinde bir float
- `kvkk_uyumlu_mu` → True değerinde bir bool

Hepsini `print()` ile ekrana yazdır.

---

## Bölüm 2 — Koleksiyonlar (Orta)

1. `desteklenen_portlar` adında bir **list** oluştur: `[22, 80, 443, 3306, 8080]`
2. Bu listeye `8443` portunu **sona ekle** (doğru metodu hatırla — append mi, add mi?)
3. `kritik_portlar` adında bir **set** oluştur: `{22, 443, 22, 3306}` (dikkat, burada tekrar var, set bunu nasıl ele alıyor gözlemle)
4. `sabit_konfigurasyon` adında bir **tuple** oluştur: `("v1.0", "production")` — neden tuple kullandığını bir yorum satırıyla açıkla
5. `host_envanteri` adında bir **dict** oluştur, şu yapıda:

```python
host_envanteri = {
    "web-01": {"ip": "192.168.1.10", "durum": "aktif", "risk_skoru": 7.2},
    "db-01": {"ip": "192.168.1.20", "durum": "aktif", "risk_skoru": 9.1},
    "test-01": {"ip": "192.168.1.30", "durum": "pasif", "risk_skoru": 2.5},
}
```

6. `host_envanteri` üzerinde bir `for` döngüsüyle gez, her host için şu formatta yazdır:
```
web-01 -> IP: 192.168.1.10, Durum: aktif, Risk: 7.2
```

---

## Bölüm 3 — Fonksiyonlar ve Ternary (Orta)

1. `risk_seviyesi_belirle(skor: float) -> str` adında bir fonksiyon yaz:
   - Skor 7.0 ve üzeriyse `"yüksek"`
   - Skor 4.0 - 6.9 arasıysa `"orta"`
   - Skor 4.0'ın altındaysa `"düşük"`
   - döndürsün

2. `host_durumu_metni(durum: str) -> str` adında bir fonksiyon yaz — **ternary (tek satır if-else)** kullanarak:
   - `durum == "aktif"` ise `"🟢 Çalışıyor"`
   - değilse `"🔴 Kapalı"`
   - döndürsün

3. Bölüm 2'deki `host_envanteri` üzerinde gezerken, artık şu formatta yazdır:
```
web-01 -> 🟢 Çalışıyor, Risk Seviyesi: yüksek
```
(yani yukarıdaki iki fonksiyonu kullanarak)

---

## Bölüm 4 — Dataclass (Orta-Zor)

1. `Host` adında bir **dataclass** tanımla, şu alanlarla:
   - `isim: str`
   - `ip: str`
   - `durum: str`
   - `risk_skoru: float`

2. Bölüm 2'deki `host_envanteri` dict'ini kullanarak, her host için bir `Host` nesnesi oluştur ve bunları bir **list** içinde topla: `host_listesi: list[Host]`

   (İpucu: dict üzerinde `for` ile gezip, her seferinde `Host(...)` oluşturup listeye `.append()` edeceksin)

3. `host_listesi` üzerinde gez, her `Host` nesnesinin `.isim` ve `.risk_skoru` alanlarına **nokta ile** erişerek yazdır.

❓ **Düşünme sorusu (yorum satırı olarak cevapla):** Neden burada dict yerine dataclass kullanmak mantıklı olabilir?

---

## Bölüm 5 — List Comprehension (Orta)

1. `host_listesi`'nden (Bölüm 4'teki), sadece **risk skoru 7.0 ve üzeri olan** host'ların **isimlerini** içeren bir liste oluştur — **comprehension** kullanarak:

```python
yuksek_riskli_hostlar = [...]  # burayı comprehension ile doldur
```

2. Aynı listeden, her host'un ismi ve risk skorunu `"isim:skor"` formatında string'e çeviren bir comprehension yaz:

```python
# Örnek çıktı: ["web-01:7.2", "db-01:9.1"]
```

---

## Bölüm 6 — Exception Handling (Zor)

1. `port_kontrol_et(port: int) -> str` adında bir fonksiyon yaz:
   - Eğer `port` 1-65535 aralığında değilse `ValueError` fırlatsın (`raise ValueError("...")`)
   - Aralıktaysa, `"Port {port} geçerli"` döndürsün

2. Bu fonksiyonu şu port listesiyle test et: `[22, 443, 99999, -5, 8080]`
   - `try/except` kullanarak her portu kontrol et
   - Geçerliyse mesajı yazdır
   - `ValueError` alırsan, `except ValueError as e:` ile yakala ve hatayı yazdır
   - `finally` bloğunda her port denemesi sonunda `"--- kontrol tamamlandı ---"` yazdır

---

## Bölüm 7 — Context Manager (Zor)

1. Bölüm 4'teki `host_listesi`'ni bir JSON dosyasına yazdıracaksın. Önce dosyanın başında şunu ekle:

```python
import json
from dataclasses import asdict   # dataclass'ı dict'e çevirmek için
```

2. `with open(...) as f:` kullanarak `host_envanteri_raporu.json` adında bir dosya oluştur, içine `host_listesi`'ndeki tüm host'ları yaz (ipucu: her `Host` nesnesini `asdict(host)` ile dict'e çevirip bir listeye topla, sonra `json.dump()` ile dosyaya yaz)

3. Sonra **aynı dosyayı tekrar** `with open(...) as f:` ile aç, `json.load()` ile oku, içeriğini `print()` ile ekrana bas.

4. `try/except` ile sarmalayarak, dosya bulunamazsa (`FileNotFoundError`) anlamlı bir hata mesajı ver.

---

## 🌟 Bonus — Recursive Function (Opsiyonel, Meraklısına)

`port_araligi_say(baslangic: int, bitis: int) -> int` adında **recursive** bir fonksiyon yaz — `baslangic`'tan `bitis`'e kadar kaç port olduğunu, döngü kullanmadan, sadece kendi kendini çağırarak hesaplasın.

(İpucu: base case ne olmalı, düşün — `baslangic > bitis` olunca durmalı)

---

## ✅ Teslim Öncesi Kontrol Listesi

- [ ] `ruff check odev1.py` — hata vermiyor (veya `--fix` ile düzelttin)
- [ ] `mypy odev1.py` — `Success: no issues found` diyor
- [ ] Kod çalışıyor, hata fırlatmıyor (Bölüm 6 hariç, orası zaten hata test ediyor)
- [ ] Her bölümün üstüne `# Bölüm X` şeklinde yorum satırı koydun (okunabilirlik için)

---

## 💡 Notlar

- Takıldığın yerde önce **kendi başına 5-10 dakika** denemeni öneririm — gerçek öğrenme orada oluyor.
- Hata mesajlarını **okumaya çalış**, Python hata mesajları genelde nerede sorun olduğunu net söyler.
- Bitirince bana gönder, satır satır review yapayım — gerçek code review gibi düşün. 😊

**Kolay gelsin! 💪**

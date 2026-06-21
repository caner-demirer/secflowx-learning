# SecFlowX Öğrenme Notları

> 10 yıllık PL/SQL geliştiricisinden siber güvenlik / Python backend geliştiriciye geçiş süreci notları.

---

## 📋 İçindekiler

1. [Faz 0 — Ortam Kurulumu](#faz-0--ortam-kurulumu)
2. [Git & GitHub Temelleri](#git--github-temelleri)
3. [Python Syntax — PL/SQL Karşılaştırmalı](#python-syntax--plsql-karşılaştırmalı)
4. [Koleksiyonlar (List, Tuple, Set, Dict)](#koleksiyonlar-list-tuple-set-dict)
5. [Kontrol Yapıları](#kontrol-yapıları)
6. [Fonksiyonlar](#fonksiyonlar)
7. [Exception Handling](#exception-handling)
8. [Recursive Function](#recursive-function)
9. [Dataclass vs Dict](#dataclass-vs-dict)
10. [List/Dict Comprehension](#listdict-comprehension)
11. [Context Manager (with)](#context-manager-with)
12. [Sanal Ortam (venv) ve Paket Yönetimi](#sanal-ortam-venv-ve-paket-yönetimi)
13. [Kod Kalite Araçları (ruff, mypy)](#kod-kalite-araçları-ruff-mypy)
14. [Asyncio — Asenkron Programlama](#asyncio--asenkron-programlama)
15. [pyproject.toml](#pyprojecttoml)

---

## Faz 0 — Ortam Kurulumu

### Kurulan Araçlar
- ✅ **VS Code** + Python extension'ları (Python, Pylance, Mypy Type Checker, Python Debugger)
- ✅ **Git** (Windows tarafında kuruldu, default editor: VS Code)
- ✅ **GitHub** hesabı (Google ile giriş)
- ✅ **WSL2 + Ubuntu** (Linux ortamı, siber güvenlik araçları için şart)
- ✅ **Docker Desktop** (WSL2 entegrasyonu aktif edildi)

### Önemli Notlar
- VS Code extension'ları **Windows** ve **WSL** tarafında **ayrı ayrı** kurulmalı. Sol altta "WSL: Ubuntu" yazıyorsa WSL ortamındasın demektir.
- WSL içinde Windows dosyalarına erişim: `/mnt/c/Users/KullaniciAdi/...`
- Windows Git config'i ile WSL Git config'i **birbirinden bağımsız** — ikisinde de `git config --global user.name/email` ayarlamak gerekir.
- Terminal açma: `Ctrl + \`` (backtick — Türkçe klavyede 1'in solunda, tilde ile aynı tuş)
- `~` karakteri: `AltGr` + sağ üstteki `+` tuşu (Türkçe Q klavye)

---

## Git & GitHub Temelleri

### SVN → Git Mapping

| SVN | Git | Ne yapar |
|---|---|---|
| `svn checkout` | `git clone` | Repoyu indir |
| `svn update` | `git pull` | Güncel hali al |
| `svn commit` | `git add .` + `git commit` | Kaydet |
| `svn status` | `git status` | Ne değişti |
| `svn log` | `git log` | Geçmiş |
| `svn revert` | `git checkout` | Geri al |

### Git'in 3 Aşaması (SVN'den Temel Fark)

SVN'de commit direkt sunucuya giderdi. Git'te **3 aşama** var:

```
Çalışma klasörün  →  Sahne (Stage)  →  Local repo  →  GitHub
   (dosyalar)         git add            git commit     git push
```

| Komut | Ne yapar | Nereye | Parametre neden var/yok |
|---|---|---|---|
| `git add .` | Hazırla | Sahneye | `.` = "bu klasördeki her şey". Git neyi ekleyeceğini bilmek zorunda |
| `git commit -m "mesaj"` | Kaydet | Bilgisayara (local) | Sadece local'de, GitHub'a gitmedi henüz |
| `git push` | Gönder | GitHub'a | Zaten commit ettiklerini biliyor, seçim gerekmez |

### Temel Komutlar

```bash
git init                          # Bu klasörü Git ile takip et (bir kere)
git status                        # Ne değişti?
git add .                         # Değişiklikleri sahneye al
git commit -m "ne yaptım"         # Kaydet (versiyon oluştur)
git log                           # Geçmiş versiyonları gör
git clone <url>                   # Repoyu indir
git push                          # GitHub'a gönder
```

### İlk Kurulum
```bash
git config --global user.name "Adın Soyadın"
git config --global user.email "email@gmail.com"
```

### Dosya/Klasör Taşıma & Yeniden Adlandırma
```bash
cp kaynak hedef        # kopyala (copy)
mv eski_isim yeni_isim # taşı / yeniden adlandır (move/rename)
```

---

## Python Syntax — PL/SQL Karşılaştırmalı

### Değişkenler ve Tipler

PL/SQL'de tip belirtmek zorundaydık:
```sql
v_isim VARCHAR2(50) := 'Caner';
v_yas NUMBER := 35;
```

Python'da tip belirtmek zorunlu değil ama modern Python'da **type hint** olarak ekliyoruz (kod kalitesi için):

```python
isim: str = "Caner"
yas: int = 35
aktif: bool = True
maas: float = 25000.50
```

`mypy` aracı bu type hint'leri kontrol eder — yanlış tip kullanırsan hata verir, PL/SQL'in compile-time kontrolüne benzer.

### Yorum Satırları (Comments)

```python
# Tek satır comment (PL/SQL'deki -- gibi)
x = 5  # satır sonunda da olabilir

"""
Çok satırlı yorum / docstring
(teknik olarak string literal, ama bu amaçla kullanılır)
"""

def topla(a: int, b: int) -> int:
    """İki sayıyı toplar ve sonucu döndürür."""  # docstring — fonksiyon açıklaması
    return a + b
```

---

## Koleksiyonlar (List, Tuple, Set, Dict)

### Genel Tablo

| Yapı | Karşılığı | Sıralı mı? | Değiştirilebilir mi? | Tekrar eden eleman? |
|---|---|---|---|---|
| `list` | Array | ✅ | ✅ | ✅ |
| `tuple` | Sabit array | ✅ | ❌ | ✅ |
| `set` | Distinct liste | ❌ | ✅ | ❌ |
| `dict` | Key-value tablo | ✅ (3.7+) | ✅ | key'ler unique, value tekrar edebilir |

⚠️ **Önemli fark**: PL/SQL'de index 1'den başlar, Python'da **0'dan** başlar.

### List

```python
zafiyetler: list[str] = ["SQL Injection", "XSS", "SSRF"]
zafiyetler.append("CSRF")          # eleman ekleme
print(zafiyetler[0])               # "SQL Injection" — index 0'dan başlar!
```

### Tuple

```python
koordinat: tuple[int, int] = (10, 20)   # değiştirilemez
```

### Set

```python
portlar: set[int] = {22, 80, 443, 443}  # tekrar eden 443 otomatik silinir
portlar.add(8080)   # SET'e eleman eklerken .add() kullanılır (list'te .append())
```

### Dict — Detaylı

**dict = key-value eşleştirmesi.** PL/SQL'de tam karşılığı yok, en yakını `INDEX BY VARCHAR2` kullanan associative array.

```python
cve_skor: dict[str, float] = {
    "CVE-2024-1234": 9.8,
    "CVE-2024-5678": 7.5
}
print(cve_skor["CVE-2024-1234"])   # 9.8
```

Dict tek bir "kayıt" değil, **birden fazla key-value çifti tutan bir mini tablo/lookup**:

| key | value |
|---|---|
| CVE-2024-1234 | 9.8 |
| CVE-2024-5678 | 7.5 |

**Karmaşık örnek — gerçek hayatta tarama sonucu:**

```python
tarama_sonucu = {
    "host": "192.168.1.10",
    "port": 443,
    "servis": "https",
    "durum": "açık",
    "zafiyetler": ["CVE-2024-1234", "CVE-2024-5678"],  # value bir liste olabilir
    "risk_skoru": 9.8
}
```

**İç içe (nested) dict** — gerçek hayatta çok kullanılır, JSON API response formatı tam bu şekildedir:

```python
asset = {
    "id": "asset-001",
    "isim": "web-server-01",
    "bulgular": [
        {"cve": "CVE-2024-1234", "skor": 9.8, "durum": "açık"},
        {"cve": "CVE-2024-5678", "skor": 5.2, "durum": "çözüldü"}
    ]
}

print(asset["bulgular"][0]["cve"])   # CVE-2024-1234
```

**Dict üzerinde gezinme:**

```python
for key, value in tarama_sonucu.items():
    print(f"{key}: {value}")
```

`.items()` hem key hem value'yu aynı anda verir — cursor'da `FOR rec IN cursor LOOP` ile `rec.kolon1, rec.kolon2`'ye erişmeye benzer.

**Dict'in süper gücü — hızlı arama (O(1)):**

```python
cve_veritabani = {
    "CVE-2024-1234": "Kritik SQL Injection",
    "CVE-2024-5678": "Orta seviye XSS"
}
aciklama = cve_veritabani["CVE-2024-1234"]   # direkt key'e zıplar, sırayla aramaz
```

**Var mı yok mu kontrolü:**

```python
if "CVE-2024-1234" in cve_veritabani:
    print("Bu CVE veritabanında var")
```

---

## Kontrol Yapıları

### If-Else

```python
yas = 35
if yas >= 18:
    print("Yetişkin")
elif yas >= 13:
    print("Genç")
else:
    print("Çocuk")
```

⚠️ Python'da `BEGIN/END` yok, noktalı virgül yok. Blok, **girintilemeyle (indentation)** belirlenir. Girinti yanlışsa kod çalışmaz.

### Ternary (Tek Satırlık If-Else)

```python
"durum": "açık" if port == 443 else "kapalı"
```

Formül:
```
DEĞER_EĞER_DOĞRU  if  KOŞUL  else  DEĞER_EĞER_YANLIŞ
```

Uzun yazımı:
```python
if port == 443:
    durum = "açık"
else:
    durum = "kapalı"
```

PL/SQL karşılığı: `CASE WHEN port = 443 THEN 'açık' ELSE 'kapalı' END`

**Ne zaman kullanılır:** Sadece basit, tek satırlık kararlar için. Karmaşık mantık varsa normal if-else daha okunaklı.

### For / While

```python
# PL/SQL'deki FOR i IN 1..10 LOOP karşılığı
for i in range(1, 11):
    print(i)

# Liste üzerinde döngü (cursor'a en yakın benzetme)
for zafiyet in zafiyetler:
    print(zafiyet)

# WHILE
sayac = 0
while sayac < 5:
    print(sayac)
    sayac += 1   # PL/SQL'de sayac := sayac + 1
```

### Matematik Operatörleri

| Operatör | Anlamı | Örnek |
|---|---|---|
| `+` | toplama | `5 + 3` → 8 |
| `-` | çıkarma | `5 - 3` → 2 |
| `*` | çarpma | `5 * 3` → 15 |
| `/` | bölme (ondalıklı) | `5 / 2` → 2.5 |
| `//` | tam bölme | `5 // 2` → 2 |
| `%` | mod (kalan) | `5 % 2` → 1 |
| `**` | üs alma | `5 ** 2` → 25 (PL/SQL'deki `POWER(5,2)`) |

---

## Fonksiyonlar

PL/SQL:
```sql
FUNCTION topla(a NUMBER, b NUMBER) RETURN NUMBER IS
BEGIN
    RETURN a + b;
END;
```

Python:
```python
def topla(a: int, b: int) -> int:
    return a + b

sonuc = topla(5, 3)
```

### `->` İşareti Ne Demek?

Fonksiyonun **ne döndüreceğini** belirten type hint.

| Parça | Anlamı |
|---|---|
| `a: int` | `a` parametresi integer olmalı |
| `-> dict` | Bu fonksiyon dict döndürür |

PL/SQL karşılığı: `RETURN tarama_rec_type` ifadesinin fonksiyon başında belirtilmesi.

⚠️ `->` sadece dokümantasyon/kontrol amaçlı — Python çalışırken bunu zorlamaz (compile-time hata vermez). `mypy` aracı kontrol eder.

### Dict Döndüren Fonksiyon Örneği

```python
def host_tara(host: str, portlar: list[int]) -> dict:
    acik_portlar = []

    for port in portlar:
        if port in [80, 443, 22]:
            acik_portlar.append(port)

    sonuc = {                              # ATAMA — sonuc değişkenine dict atanıyor
        "host": host,
        "taranan_port_sayisi": len(portlar),
        "acik_portlar": acik_portlar,
        "risk_seviyesi": "yüksek" if 22 in acik_portlar else "düşük"
    }

    return sonuc                           # dict dışarı gönderiliyor

# Kullanım
hedef_portlar = [22, 80, 443, 8080, 3306]
rapor = host_tara("192.168.1.10", hedef_portlar)   # 2. ATAMA — dönen dict, rapor'a atanıyor

print(rapor)
print(rapor["acik_portlar"])      # [22, 80, 443]
print(rapor["risk_seviyesi"])     # yüksek
```

**Not:** `rapor` özel bir keyword değil, sadece bizim seçtiğimiz bir değişken ismi. Fonksiyonun döndürdüğü dict'i bir değişkende tutuyoruz ki sonradan kullanabilelim.

---

## Exception Handling

PL/SQL:
```sql
BEGIN
    -- işlem
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Bulunamadı');
    WHEN OTHERS THEN
        RAISE;
END;
```

Python:
```python
try:
    sonuc = 10 / 0
except ZeroDivisionError:              # standart/spesifik exception
    print("Sıfıra bölme hatası")
except Exception as e:                 # e değişkeninin içine hata mesajı gelir
    print(f"Beklenmeyen hata: {e}")
finally:                               # kod hata verse de vermese de çalışan bölüm
    print("Her durumda çalışır")       # genelde dosya kapatma gibi temizlik işleri için
```

### `except ... as e` Nedir?

`e`, yakalanan hata nesnesini (exception object) tutan bir değişken — hatanın detayını görmek için. PL/SQL karşılığı: `SQLERRM`.

### `finally` Nedir?

Hata olsun ya da olmasın **her durumda çalışır.** Temizlik işlemleri için kullanılır (dosya kapatma, bağlantı kesme).

### ⚠️ Sıralama Kuralı

Önce **spesifik** hata, sonra **genel** hata olmalı:

```python
except ZeroDivisionError:   # önce spesifik
    ...
except Exception as e:       # sonra genel
    ...
```

Tersi olursa, genel olan her şeyi yakalar, spesifik olana asla ulaşılmaz (ölü kod). PL/SQL'de `WHEN NO_DATA_FOUND` önce, `WHEN OTHERS` en sonda olması ile aynı mantık.

---

## Recursive Function

SQL'deki Recursive CTE'nin Python karşılığı: **fonksiyonun kendi kendini çağırması.**

### SQL Recursive CTE (hatırlatma)
```sql
WITH RECURSIVE org_chart AS (
    SELECT id, isim, yonetici_id FROM calisanlar WHERE yonetici_id IS NULL
    UNION ALL
    SELECT c.id, c.isim, c.yonetici_id
    FROM calisanlar c JOIN org_chart o ON c.yonetici_id = o.id
)
SELECT * FROM org_chart;
```

### Python'da Recursive Function

```python
def faktoriyel(n: int) -> int:
    if n <= 1:        # durma koşulu (base case)
        return 1
    return n * faktoriyel(n - 1)   # kendi kendini çağırıyor

print(faktoriyel(5))   # 120
```

### Gerçek Kullanım: Klasör Tarama

```python
import os
# os = "operating system" — işletim sistemiyle Python üzerinden etkileşim kurma modülü
# (subprocess'ten farklı: os GERÇEK terminal komutu çalıştırmaz, kendi hazır fonksiyonlarını kullanır)

def klasor_tara(yol: str, derinlik: int = 0):
    # derinlik: int = 0 → varsayılan değer, çağırırken belirtmezsen otomatik 0 olur
    # PL/SQL'deki DEFAULT 0 parametre tanımına benzer

    for eleman in os.listdir(yol):
        # os.listdir(yol) → o klasörün içindekilerin isimlerini LİSTE olarak döner

        tam_yol = os.path.join(yol, eleman)
        # os.path.join() → klasör yolu ile dosya/klasör ismini birleştirir
        # Windows'ta \ Linux'ta / kullanır, senin yerine bunu halleder

        print("  " * derinlik + eleman)
        # "  " * derinlik → boşluğu derinlik kadar tekrarlar (görsel girintileme için)

        if os.path.isdir(tam_yol):
            # os.path.isdir() → verilen yol bir klasör mü diye kontrol eder (True/False)

            klasor_tara(tam_yol, derinlik + 1)
            # RECURSIVE ÇAĞRI — fonksiyon kendi kendini, bir alt seviye derinlikle çağırıyor

klasor_tara("/home/caner/projeler")
```

### ⚠️ Base Case (Durma Koşulu) Şart!

Recursive CTE'de `UNION ALL` ile bağlanan kısım bir noktada bitiyorsa, Python'da da bir noktada **durması gereken bir koşul** olmalı. Yoksa sonsuz döngüye girer, `RecursionError` alırsın.

### `os` vs `subprocess` Farkı

| Modül | Ne yapar | Örnek |
|---|---|---|
| `os` | Dosya/klasör/ortam ile Python üzerinden ilişki kurar | `os.listdir()`, `os.getcwd()` |
| `subprocess` | **Gerçek terminal komutları** çalıştırır | `subprocess.run(["nmap", ...])` |

SecFlowX'te Trivy/Nmap gibi araçları Python'dan çağırırken (Faz 3) `subprocess` kullanılacak.

---

## Dataclass vs Dict

### Dataclass — Dict'in Daha Düzenli/Tip Güvenli Hali

Dict'in sorunu: yazım hatası (`sonuc["hsot"]`) fark edilmez, çalışana kadar anlaşılmaz, tip kontrolü yok.

```python
from dataclasses import dataclass

@dataclass
class TaramaSonucu:
    host: str
    port: int
    durum: str

# Kullanım
sonuc = TaramaSonucu(host="192.168.1.10", port=443, durum="açık")

print(sonuc.host)     # NOKTA ile erişim — sonuc.host (dict["host"] DEĞİL!)
print(sonuc.port)
```

PL/SQL karşılığı:
```sql
TYPE tarama_rec_type IS RECORD (
    host    VARCHAR2(50),
    port    NUMBER,
    durum   VARCHAR2(20)
);
v_sonuc tarama_rec_type;
v_sonuc.host := '192.168.1.10';
```

### ⚠️ Erişim Şekli Farkı — KRİTİK

| Yapı | Erişim |
|---|---|
| `dict` | `rapor["durum"]` — köşeli parantez |
| `dataclass` | `sonuc.durum` — nokta |

Bunlar birbirinin yerine geçmez. Dict'i nokta ile, dataclass'ı köşeli parantez ile okumaya çalışırsan **hata alırsın.** Önemli olan değişkenin adı değil, **tipi** (dict mi, dataclass mı).

### Neden Hâlâ Dict Kullanıyoruz (Dataclass Varken)?

| Senaryo | Kullan |
|---|---|
| Dış kaynaktan gelen veri (JSON, API response) | `dict` |
| Kendi sistemin içinde, tip güvenliği istenen yer | `dataclass` / Pydantic |
| Hızlı, geçici, basit veri | `dict` |
| Sabit yapılı, tekrar kullanılan model | `dataclass` |

**Neden:** Bir API'den veya tarama aracından (Nmap, Trivy) gelen veri JSON formatındadır, Python'a girince otomatik **dict** olur:

```python
import json
veri = json.loads('{"host": "1.2.3.4", "port": 443}')
print(type(veri))   # <class 'dict'>
```

Dict ayrıca **esnektir** — her zaman aynı key'lere sahip olmak zorunda değil (bazı taramalarda `risk_skoru` olur, bazılarında olmaz). Dataclass'ta her alan sabit olmalı.

**Gerçek akış (SecFlowX'te göreceğin):**
```python
# 1. Dış kaynaktan JSON gelir → otomatik dict olur
ham_veri = json.loads(trivy_ciktisi)   # dict

# 2. Kendi sistemine alırken dataclass/Pydantic modeline çeviririz (tip güvenliği için)
sonuc = TaramaSonucu(host=ham_veri["host"], port=ham_veri["port"])

# 3. Artık sonuc.host, sonuc.port ile güvenle çalışırız
```

---

## List/Dict Comprehension

PL/SQL'de tam karşılığı yok (en yakını BULK COLLECT, ama syntax çok farklı) — Python'a özgü yeni bir kavram olarak öğrenildi.

### Normal For Döngüsü vs Comprehension

```python
# Normal yöntem
sayilar = [1, 2, 3, 4, 5]
karesi = []
for sayi in sayilar:
    karesi.append(sayi ** 2)

# Comprehension ile (tek satır)
karesi = [sayi ** 2 for sayi in sayilar]
print(karesi)   # [1, 4, 9, 16, 25]
```

**Formül:** `[ifade for eleman in liste]`
Okunuşu: *"liste içindeki her eleman için, ifadeyi hesapla, yeni listeye koy"*

### Koşullu Comprehension (Filtreleme)

```python
portlar = [22, 80, 443, 3306, 8080]

# Normal yöntem
acik_portlar = []
for port in portlar:
    if port in [80, 443]:
        acik_portlar.append(port)

# Comprehension ile
acik_portlar = [port for port in portlar if port in [80, 443]]
```

**Formül:** `[ifade for eleman in liste if koşul]`

### Dict Comprehension

```python
cve_listesi = ["CVE-2024-1234", "CVE-2024-5678"]
cve_skorlari = {cve: 0.0 for cve in cve_listesi}
# {'CVE-2024-1234': 0.0, 'CVE-2024-5678': 0.0}
```

### Ne Zaman Kullanılır?

- ✅ Basit, kısa dönüşümler için harika
- ❌ Karmaşık mantık varsa (birden fazla if, nested loop) okunaklılık bozulur — normal for döngüsü tercih edilmeli

---

## Context Manager (with)

**Mantık:** Bir kaynağı aç, işini yap, mutlaka kapat — hata olsa bile.

### Yanlış/Eski Yöntem

```python
dosya = open("rapor.txt")
veri = dosya.read()
dosya.close()   # bunu unutursan dosya açık kalır, hata olursa close()'a hiç ulaşılmaz
```

### `with` ile Doğru Yöntem

```python
with open("rapor.txt") as dosya:
    veri = dosya.read()
# buradan çıkınca dosya OTOMATİK kapanır, hata olsa bile
```

`with` bloğu bitince (veya içinde hata çıksa bile) kaynağı otomatik temizler — bir nevi otomatik `finally` mantığı içinde barındırır.

### ⚠️ `with` Hatayı YAKALAMAZ, Sadece Kaynağı Kapatır

`with` ve `try/except` **farklı görevler** görür, birlikte kullanılmalı:

| Yapı | Görevi |
|---|---|
| `with` | Kaynağı (dosya, bağlantı) otomatik kapat — hata olsa da olmasa da |
| `try/except` | Hatayı yakala, programın çökmesini engelle |

```python
try:
    with open("olmayan_dosya.txt") as dosya:
        veri = dosya.read()
except FileNotFoundError as e:
    print(f"Dosya bulunamadı: {e}")
```

İkisi birlikte kullanıldığında: `with` bloğu içinde hangi hata olursa olsun, dosya önce düzgünce kapanır, sonra hata `except`'e fırlatılır.

```python
try:
    with open("rapor.txt") as dosya:
        veri = dosya.read()
        sonuc = 10 / 0
except FileNotFoundError as e:
    print(f"Dosya hatası: {e}")
except ZeroDivisionError as e:
    print(f"Hesap hatası: {e}")
finally:
    print("İşlem tamamlandı")
```

### SecFlowX'teki Kullanım Alanları

```python
# Dosyaya tarama sonucu yazma
with open("tarama_sonucu.json", "w") as f:
    f.write(json.dumps(sonuc))

# Veritabanı bağlantısı (SQLAlchemy'de göreceğiz)
with db.session() as session:
    session.add(yeni_kayit)
    session.commit()
```

---

## Sanal Ortam (venv) ve Paket Yönetimi

### `venv` Neden Gerekli?

PL/SQL'de farklı projeler için farklı paket versiyonu sorunu pek yaşanmaz. Python'da ciddi bir sorun:

> Proje A, `requests` kütüphanesinin 2.0 versiyonunu ister. Proje B aynı kütüphanenin 3.0 versiyonunu ister. İkisini de global kurarsan çakışırlar.

**`venv`** = her proje için izole bir Python ortamı oluşturur. Proje A'nın kütüphaneleri Proje B'yi etkilemez.

### Kurulum ve Kullanım Adımları

```bash
# 1. Proje klasörü oluştur
mkdir secflowx-proje
cd secflowx-proje

# 2. Sanal ortam oluştur (gerekirse önce: sudo apt install python3.14-venv -y)
python3 -m venv venv

# 3. Aktif et — prompt'ta (venv) görünür
source venv/bin/activate

# 4. Paket kur (artık sadece bu projeye ait)
pip install requests

# 5. Kurulu paketleri listele
pip list

# 6. Bağımlılıkları dosyaya kaydet (proje paylaşımı için)
pip freeze > requirements.txt
```

### `requirements.txt` Ne İşe Yarar?

```
certifi==2026.6.17
charset-normalizer==3.4.7
idna==3.18
requests==2.34.2
urllib3==2.7.0
```

Her satır: **paket adı == versiyon**. Bu dosyayı paylaşırsan (GitHub'a push ederek), başka biri (veya başka bir bilgisayar) şu komutla **aynı ortamı tek seferde** kurabilir:

```bash
pip install -r requirements.txt
```

PL/SQL'de bir kurulum script'i paylaşmak gibi düşünebilirsin — "bu projeyi çalıştırmak için şunlar lazım" listesi.

### ⚠️ Önemli: `venv` Klasörü Git'e Eklenmez

`venv` klasörü binlerce dosya içerir ve her bilgisayarda `requirements.txt` üzerinden yeniden oluşturulabilir. Bu yüzden Git'e **asla eklenmez** — `.gitignore` dosyasıyla hariç tutulur (bu konu henüz işlenmedi, ileride detaylandırılacak).

### 📌 Pratik Not

Projeleri **WSL/Ubuntu home dizininde** (`~/secflowx-proje` gibi) tutmak, Windows tarafında (`/mnt/c/...`) tutmaktan performans ve uyumluluk açısından daha iyidir.

---

## Kod Kalite Araçları (ruff, mypy)

PL/SQL Developer / SQL Developer'ın seni yazım hatalarına karşı uyarması gibi düşün — Python dünyasında bu işi **bağımsız, ayrı araçlar** yapıyor (IDE'nin kendisi değil).

### Kurulum

```bash
cd ~/secflowx-proje
source venv/bin/activate
pip install ruff mypy
```

### `ruff` — Lint + Format

İki işi var:
1. **Lint** — kod kalitesi kontrolü (kullanılmayan import, hatalı pattern'ler)
2. **Format** — kodu otomatik düzenli hale getirir

```bash
ruff check .              # kontrol et, sorunları listele
ruff check . --fix        # otomatik düzeltilebilenleri düzelt
ruff format .              # kodu otomatik biçimlendir
```

**Örnek — yakaladığı hata:**
```python
import os
import sys   # kullanılmıyor

def topla(a: int, b: int) -> int:
    return str(a + b)
```

```bash
ruff check test_kalite.py
```
Çıktı:
```
F401 `os` imported but unused
F401 `sys` imported but unused
Found 2 errors.
[*] 2 fixable with the --fix option.
```

### `mypy` — Statik Tip Kontrolü

Type hint'leri **gerçekten kontrol eden** araç — PL/SQL'in compile-time tip kontrolüne en yakın Python karşılığı. Python normalde "yazarken kontrol etmez", `mypy` bu eksikliği kapatır.

```bash
mypy dosya.py
```

**Örnek — yakaladığı hata:**
```python
def topla(a: int, b: int) -> int:
    return str(a + b)   # YANLIŞ! int demiştik, str döndürüyoruz
```

Çıktı:
```
test_kalite.py:3: error: Incompatible return value type (got "str", expected "int")  [return-value]
Found 1 error in 1 file (checked 1 source file)
```

Düzeltilince (`return a + b`):
```
Success: no issues found in 1 source file
```

### Neden Önemli?

Gerçek projelerde bu araçlar genelde **otomatikleştirilir**, elle çalıştırılmaz:

| Yöntem | Ne zaman çalışır |
|---|---|
| VS Code "format on save" | `Ctrl+S` yapınca otomatik |
| Pre-commit hook | `git commit` atmadan önce |
| CI/CD (GitHub Actions) | `git push` sonrası, sunucuda |

Takım çalışmasında kod stilini tutarlı tutmak ve tip hatalarını production'a kadar fark edilmeden bırakmamak için standart pratik.

---

## Asyncio — Asenkron Programlama

PL/SQL'den **en uzak** olan kavram — PL/SQL tamamen senkron (sıralı) bir dünya, Python'da `asyncio` ile paralel bekleme mantığı var.

### Senkron (Normal) Kod Nasıl Çalışır?

```python
import time

def kahve_yap():
    print("Kahve hazırlanıyor...")
    time.sleep(3)
    print("Kahve hazır!")

def ekmek_kizart():
    print("Ekmek kızartılıyor...")
    time.sleep(2)
    print("Ekmek hazır!")

kahve_yap()
ekmek_kizart()
```

**Toplam süre: 5 saniye** (3+2) — kahve bitmeden ekmeğe başlanmıyor, PL/SQL'deki her satırın sırayla çalışması gibi.

### Fonksiyon Çağırma Hatırlatması

```python
kahve_yap      # ❌ fonksiyonu ÇAĞIRMAZ, sadece referans verir
kahve_yap()    # ✅ fonksiyonu ÇALIŞTIRIR — parantez şart
```

Python'da parametre olsun olmasın **parantez her zaman gereklidir** (PL/SQL'de parametresiz çağrıda parantez gerekmeyebilir, Python'da hep gerekir).

### Neden Asyncio Gerekli? (Gerçek Hayat Mantığı)

Kahve makinesi demlerken biz beklemeyiz, o sırada ekmeği de kızartmaya başlarız — **aynı anda iki "bekleme" işini yürütürüz.** `asyncio` bu mantığı koda taşır, özellikle **I/O bekleme** durumlarında (network isteği, dosya okuma, veritabanı sorgusu).

### `async` / `await` Syntax'ı

```python
import asyncio

async def kahve_yap():                  # "async def" ile tanımlanan = coroutine
    print("Kahve hazırlanıyor...")
    await asyncio.sleep(3)               # asenkron bekleme — "ben beklerken sen başka iş yap"
    print("Kahve hazır!")

async def ekmek_kizart():
    print("Ekmek kızartılıyor...")
    await asyncio.sleep(2)
    print("Ekmek hazır!")

async def main():
    await asyncio.gather(                # birden fazla async işi AYNI ANDA başlatır
        kahve_yap(),
        ekmek_kizart()
    )

asyncio.run(main())                      # async kodun giriş kapısı
```

`time.sleep()` programı **tamamen durdurur**; `asyncio.sleep()` ise "bekliyorum ama sen bu arada başka iş yapabilirsin" der.

**Sonuç:** Senkron versiyon 5 saniye sürerken, async versiyon **~3 saniyede** biter (en uzun süren işlem kadar, ikisi paralel ilerlediği için).

### SecFlowX İçin Neden Kritik?

100 farklı host taranacağını düşün, her birine network isteği atılıp cevap bekleniyor:

- **Senkron:** Host 1'i tara, bitince Host 2... → 100 × 2 saniye = **200 saniye**
- **Async:** Hepsini aynı anda başlat, hepsi paralel bekler → **~2-3 saniye**

Dökümandaki *"tarayıcılar I/O-bound iştir"* notu tam bu yüzden — bekleme süresini paralelleştirmek devasa hız kazandırır.

---

## pyproject.toml

`requirements.txt`'in daha gelişmiş, modern hali — projenin **tüm kimliğini** (ad, versiyon, Python sürümü, bağımlılıklar, araç ayarları) tek dosyada toplar. PL/SQL'de bir paket spesifikasyonu gibi düşünebilirsin.

### Karşılaştırma

```
# requirements.txt — sadece paket listesi
requests==2.34.2
fastapi==0.115.0
```

```toml
# pyproject.toml — projenin TÜM kimliği
[project]
name = "secflowx-proje"
version = "0.1.0"
description = "SecFlowX ogrenme projesi"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.34.2",
    "fastapi>=0.115.0",
]

[tool.ruff]
line-length = 100

[tool.mypy]
strict = true
```

| `requirements.txt` | `pyproject.toml` |
|---|---|
| Sadece paket versiyonları | Proje adı, versiyon, Python sürümü, paketler |
| `ruff`/`mypy` ayarları ayrı dosyalarda | Hepsi tek dosyada toplanır |
| Eski yöntem ama hâlâ yaygın | Modern, güncel standart |

FastAPI projesine geçince (Hafta 2) gerçek kullanımı görülecek — `pip install -e .` ile bu dosyadan kurulum yapılabiliyor.

---

## 🎯 Faz 1 — Hafta 1 Durumu: ✅ TAMAMLANDI

- [x] Modern Python syntax (type hints, dataclass, comprehension, context manager, exception handling)
- [x] `venv`, `pip`, `requirements.txt`
- [x] `ruff`, `mypy`
- [x] `asyncio` mantığı
- [x] `pyproject.toml` (kavramsal giriş)
- [ ] `.gitignore` kullanımı (sıradaki pratik konu)

## 🎯 Sıradaki Konular (Faz 1 — Hafta 2)

- [ ] FastAPI temelleri: path/query parametreleri, request/response modelleri
- [ ] Pydantic ile veri doğrulama ve serialization
- [ ] Dependency injection, middleware, hata yönetimi
- [ ] Kimlik doğrulama: JWT, OAuth2 password flow, RBAC
- [ ] `httpx` ile dış servislere async istek

---

*Bu döküman, Claude ile yapılan interaktif öğrenme oturumlarının özetidir. SecFlowX Ekibi Öğrenme Yol Haritası'nın Faz 0 ve Faz 1 (tamamı) bölümlerini kapsar.*

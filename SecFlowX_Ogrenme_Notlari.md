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

---

## FastAPI Temelleri (Faz 1 — Hafta 2 Başlangıç)

### FastAPI Nedir?

Python ile **REST API** yazmak için kullanılan modern bir framework. SecFlowX'te tarama sonuçlarını, asset'leri, bulguları dışarıya sunan API katmanı tam olarak bu.

PL/SQL dünyasında en yakın karşılığı: **Oracle REST Data Services (ORDS)** — veritabanını HTTP endpoint'leri üzerinden dışarıya açmak. FastAPI de aynı mantık ama çok daha esnek.

### Kurulum

```bash
pip install fastapi uvicorn
```

`uvicorn` = FastAPI'yi çalıştıran web sunucusu.

### İlk API

```python
from fastapi import FastAPI

app = FastAPI()        # uygulamayı oluştur

@app.get("/")          # GET isteğini yakala — decorator
def root():
    return {"mesaj": "SecFlowX API çalışıyor!"}   # dict döndür → otomatik JSON olur
```

Çalıştırma:
```bash
uvicorn main:app --reload
```

`--reload` = kod değişince otomatik yeniden başlar (geliştirme için).

### `@app.get("/")` — Decorator Nedir?

`@` işareti ile başlayan şeylere **decorator** deniyor — fonksiyonun davranışını değiştiriyor. Burada şunu söylüyor:

> "Bu fonksiyon, `/` adresine gelen **HTTP GET** isteğine cevap versin."

### HTTP Metodları

| Decorator | HTTP Metodu | Ne için |
|---|---|---|
| `@app.get` | GET | Veri okuma |
| `@app.post` | POST | Veri oluşturma |
| `@app.put` | PUT | Veri güncelleme |
| `@app.delete` | DELETE | Veri silme |

### Yaygın HTTP Status Kodları

| Kod | Anlamı |
|---|---|
| `200` | Başarılı |
| `201` | Oluşturuldu (POST sonrası) |
| `400` | Hatalı istek (client hatası) |
| `401` | Yetkisiz |
| `404` | Bulunamadı |
| `500` | Sunucu hatası |

### Swagger UI — Otomatik Dokümantasyon

FastAPI'nin süper gücü — hiçbir şey yazmadan endpoint'leri okuyup **interaktif dokümantasyon** oluşturur:

```
http://127.0.0.1:8000/docs
```

Buradan endpoint'leri test edebilir, curl komutlarını görebilir, response'ları inceleyebilirsin. PL/SQL'de bunu manuel yazman gerekirdi.

---

## FastAPI — Path & Query Parameter

### Path Parameter
URL'in içine gömülen zorunlu parametre. Süslü parantez ile tanımlanır.

```python
@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str):
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if ip_adresi in ozel_ipler else "dış ağ"
    return {"sorgu": ip_adresi, "durum": durum}
```

- `{ip_adresi}` ile fonksiyon parametre ismi birebir aynı olmalı — farklı olursa hata
- PL/SQL'deki `p_ip IN VARCHAR2` ile aynı mantık, sadece URL'den geliyor

### Query Parameter
`?` işaretinden sonra gelen opsiyonel parametre. URL'de `?` ile başlar.

```python
@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str, detay: bool = False):
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if ip_adresi in ozel_ipler else "dış ağ"
    sonuc: dict[str, str | int] = {"sorgu": ip_adresi, "durum": durum}
    if detay:
        sonuc["port_sayisi"] = 1024
        sonuc["protokol"] = "TCP"
    return sonuc
```

- URL: `/host/192.168.1.1?detay=true`
- Default değer verilirse opsiyonel — PL/SQL'deki `DEFAULT FALSE` ile aynı mantık
- YouTube'daki `?v=YMphjbxKCS0` ile aynı yapı, web'de her yerde bu format var

### Path vs Query Farkı

| | Path Parameter | Query Parameter |
|---|---|---|
| URL'de yeri | `/host/{ip}` | `?detay=true` |
| Zorunlu mu? | ✅ Evet | ❌ Hayır, default alabilir |
| Ne için | Kaynağı tanımlar | Filtreleme, ek seçenek |

### dict karışık tip notu
Dict içine hem `str` hem `int` girecekse:
```python
sonuc: dict[str, str | int] = {"sorgu": ip_adresi, "durum": durum}
```
Gerçek hayatta bu noktada Pydantic modeline geçilir.

---

## FastAPI — Pydantic ile Response Modeli

Fonksiyonun ne döndüreceğini önceden tanımlamak için kullanılır. Dict'in tip güvenli ve belgelenmiş hali.

```python
from pydantic import BaseModel

class HostSonuc(BaseModel):
    sorgu: str
    durum: str
    port_sayisi: int | None = None
    protokol: str | None = None
```

- `str` → zorunlu alan (`*` ile gösterilir Swagger'da)
- `int | None = None` → opsiyonel alan, verilmezse `null` döner
- PL/SQL'deki `NUMBER DEFAULT NULL` ile aynı mantık

### Fonksiyonda Kullanım

```python
@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str, detay: bool = False) -> HostSonuc:
    ozel_ipler = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    durum = "iç ağ" if ip_adresi in ozel_ipler else "dış ağ"

    if detay:
        return HostSonuc(sorgu=ip_adresi, durum=durum, port_sayisi=1024, protokol="TCP")

    return HostSonuc(sorgu=ip_adresi, durum=durum)
```

- `-> HostSonuc` → fonksiyonun ne döndüreceği artık belgelenmiş
- Dict dönerken Swagger hiçbir şey bilmiyordu, şimdi schema otomatik oluşuyor
- Opsiyonel alanlar verilmezse `null` olarak döner — dict'te hiç gelmiyordu

### Dict vs Pydantic Farkı

| | Dict | Pydantic |
|---|---|---|
| Swagger'da schema | ❌ Yok | ✅ Otomatik oluşur |
| Tip kontrolü | ❌ Yok | ✅ Var |
| Opsiyonel alan | Hiç gelmez | `null` olarak gelir |
| Erişim | `sonuc["sorgu"]` | `sonuc.sorgu` |

---

## FastAPI — HTTP Hata Kodları ve HTTPException

### Hata Kodları Mantığı
- **4xx** → kullanıcı hatası — yanlış/geçersiz istek gönderdi
- **5xx** → sunucu hatası — kodumuzda bir şey patladı
- **400** → Bad Request — gönderilen veri geçersiz
- **404** → Not Found — aranan kaynak bulunamadı
- **422** → FastAPI'nin otomatik verdiği, tip uyuşmazlığı

### HTTPException Kullanımı
```python
from fastapi import FastAPI, HTTPException

raise HTTPException(status_code=400, detail="Geçersiz IP adresi")
```
PL/SQL'deki `RAISE_APPLICATION_ERROR` gibi — normal akışı durdurup hata fırlatır.

### IP Doğrulama
```python
parcalar = ip_adresi.split(".")
if len(parcalar) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parcalar):
    raise HTTPException(status_code=400, detail="Geçersiz IP adresi")
```
- `split(".")` → stringi noktalara göre böler, liste döndürür
- `len()` → string, liste, dict için eleman sayısı döndürür — PL/SQL'deki `LENGTH`'ten farklı, her tip için çalışır
- `all()` → listedeki her eleman için koşul kontrolü yapar
- `isdigit()` → string sadece rakamlardan mı oluşuyor
- `0 <= int(p) <= 255` → PL/SQL'deki `p BETWEEN 0 AND 255` ile aynı

### 404 — Kayıt Bulunamadı
```python
kayitli_hostlar = {
    "192.168.1.1": "router",
    "10.0.0.1": "firewall",
    "172.16.0.1": "switch"
}

if ip_adresi not in kayitli_hostlar:
    raise HTTPException(status_code=404, detail="Host bulunamadı")

cihaz = kayitli_hostlar[ip_adresi]
```
- `kayitli_hostlar` → modül seviyesinde tanımlı dict, tüm endpoint'ler erişebilir — PL/SQL paketindeki global değişken gibi
- 404 → FastAPI routing'de endpoint yoksa otomatik verir, kayıt yoksa sen verirsin

### POST Endpoint — Request Body
```python
class TaramaIstegi(BaseModel):
    ip_adresi: str
    port: int = 80
    protokol: str = "TCP"

@app.post("/tara")
def tara(istek: TaramaIstegi) -> HostSonuc:
    ...
    return HostSonuc(sorgu=istek.ip_adresi, durum=durum, port_sayisi=istek.port, protokol=istek.protokol)
```
- GET'te parametre URL'de görünür, POST'ta body'de JSON olarak gelir
- `istek.ip_adresi` → Pydantic objesi, nokta ile erişilir — dict'teki `istek["ip_adresi"]`'nden farkı bu
- Swagger'da GET edit box gösterir, POST text editör gösterir — parametre sayısıyla alakalı değil, verinin nerede taşındığıyla alakalı

### FastAPI Routing Tablosu
`@app.get`, `@app.post` decorator'ları FastAPI'nin routing tablosunu oluşturur:
GET  /              → root
GET  /host/{ip}     → host_sorgula
POST /tara          → tara

Biri istek attığında FastAPI bu tabloya bakar — URL eşleşmiyorsa otomatik 404 verir.

---

## FastAPI — Dependency Injection

Tekrar eden kodları tek yerde toplayıp endpoint'lere otomatik enjekte etmek için kullanılır.

```python
from fastapi import Depends

def ip_dogrula(ip_adresi: str) -> str:
    parcalar = ip_adresi.split(".")
    if len(parcalar) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parcalar):
        raise HTTPException(status_code=400, detail="Geçersiz IP adresi")
    return ip_adresi

@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str = Depends(ip_dogrula), detay: bool = False) -> HostSonuc:
    ...
```

- `Depends(ip_dogrula)` → "bu parametre gelince önce ip_dogrula çalıştır, sonucu ver" demek
- FastAPI önce dependency'i çalıştırır, hata yoksa endpoint'e girer
- POST'ta body içindeki IP için direkt fonksiyon çağrısı yapılır: `ip_dogrula(istek.ip_adresi)`
- Yardımcı fonksiyonlar her zaman kullananlardan önce tanımlanmalı — Python dosyayı yukardan aşağı okur

---

## FastAPI — JWT Kimlik Doğrulama

### Kurulum
```bash
pip install python-jose[cryptography] bcrypt==4.0.1
```

### Global Ayarlar
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import bcrypt

GIZLI_ANAHTAR = "secflowx-super-gizli-anahtar-2024"  # gerçek projede gizli tutulur, koda yazılmaz
ALGORITMA = "HS256"  # HMAC-SHA256
TOKEN_SURESI = 30  # dakika

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/giris")

sahte_kullanicilar = {
    "caner": {
        "kullanici_adi": "caner",
        "sifre_hash": bcrypt.hashpw("sifre123".encode(), bcrypt.gensalt()).decode()
    }
}
```

### Token Oluşturma ve Doğrulama
```python
def token_olustur(veri: dict) -> str:
    payload = veri.copy()  # .copy() — orijinal dict'i bozmamak için, Python'da dict'ler referans ile çalışır
    bitis = datetime.utcnow() + timedelta(minutes=TOKEN_SURESI)
    payload.update({"exp": bitis})  # exp → token bitiş zamanı, JWT standardı
    return jwt.encode(payload, GIZLI_ANAHTAR, algorithm=ALGORITMA)

def token_dogrula(token: str) -> str:
    try:
        payload = jwt.decode(token, GIZLI_ANAHTAR, algorithms=[ALGORITMA])
        kullanici = payload.get("sub")  # sub → "subject", kimin tokeni, JWT standardı
        if kullanici is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        return kullanici
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")
```

### Giriş Endpoint'i
```python
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
```

### Korumalı Endpoint
```python
@app.get("/host/{ip_adresi}")
def host_sorgula(ip_adresi: str = Depends(ip_dogrula), detay: bool = False, token: str = Depends(oauth2_scheme)) -> HostSonuc:
    kullanici = token_dogrula(token)
    ...
```
- `Depends(oauth2_scheme)` → header'daki `Authorization: Bearer <token>` otomatik okunur
- Token yoksa → 401 "Not authenticated"
- Token geçersizse → 401 "Geçersiz token"
- Token geçerliyse → endpoint çalışır

### JWT Yapısı
Token üç parçadan oluşur, nokta ile ayrılır:
- **Header** → algoritma bilgisi
- **Payload** → içindeki veri `{"sub": "caner", "exp": ...}`
- **Signature** → gizli anahtar ile imzalanmış, sahte token oluşturulamaz

### Terminal ile Test
```bash
# Token al
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/giris \
  -H "Content-Type: application/json" \
  -d '{"kullanici_adi": "caner", "sifre": "sifre123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Token ile istek at
curl -X GET http://127.0.0.1:8000/host/192.168.1.1 \
  -H "Authorization: Bearer $TOKEN"
```

### Akış
POST /giris  → kullanıcı adı + şifre gönder
API          → token döndür (30 dakika geçerli)
GET /host/.. → Authorization: Bearer <token> header ile istek at
API          → token geçerliyse cevap ver, değilse 401

### passlib uyumsuzluk notu
Python 3.14 ile `passlib[bcrypt]` uyumsuz — direkt `bcrypt==4.0.1` kullan.

Tamam. Şimdi notları ekle. SecFlowX_Ogrenme_Notlari.md dosyasında ## FastAPI — JWT Kimlik Doğrulama bölümünün altına şunu ekle:
markdown---

## FastAPI — httpx ile Dış Servis Entegrasyonu

Dış API'lere async istek atmak için `httpx` kullanılır.

### Kurulum
```bash
pip install httpx
```

### Kullanım
```python
import httpx

@app.get("/dis-servis/{ip_adresi}")
async def dis_servis_sorgula(ip_adresi: str = Depends(ip_dogrula)):
    async with httpx.AsyncClient() as client:
        yanit = await client.get(f"http://ip-api.com/json/{ip_adresi}")
    return {"ip": ip_adresi, "dis_servis_yaniti": yanit.json()}
```

- `async with httpx.AsyncClient() as client` → context manager, blok bitince bağlantı otomatik kapanır — `with open(...) as f` ile aynı mantık
- `await client.get(...)` → isteği gönder, cevap gelene kadar bekle ama beklerken başka işlere bak
- `yanit.json()` → gelen cevabı Python dict'ine çevirir — `json.loads()` ile aynı
- Endpoint `async def` olmalı — `await` kullanabilmek için

### ip-api.com — Ücretsiz IP Bilgi Servisi
http://ip-api.com/json/8.8.8.8

Döndürdüğü bilgiler: ülke, şehir, bölge, ISP, koordinat, timezone

Siber güvenlikte buna **OSINT** (Open Source Intelligence) denir — açık kaynaklardan istihbarat toplama.

### Not
- `https://httpbin.org` test servisi bazen çöküyor — alternatif olarak `ip-api.com` kullan
- `ip-api.com` SSL'i ücretli sunuyor — `http://` ile kullan, `https://` çalışmaz

---

## Faz 1 — Hafta 3: Veri Katmanı

---

## PostgreSQL + Docker

PostgreSQL'i Docker ile ayağa kaldırmak:

```bash
docker run --name secflowx-db \
  -e POSTGRES_USER=secflowx \
  -e POSTGRES_PASSWORD=secflowx123 \
  -e POSTGRES_DB=secflowx \
  -p 5432:5432 \
  -d postgres:16
```

Sonraki oturumlarda container durmuş olabilir, başlatmak için:
```bash
docker start secflowx-db
```

Tabloları kontrol etmek için:
```bash
docker exec -it secflowx-db psql -U secflowx -d secflowx -c "\dt"
```

### PostgreSQL vs Oracle Farkları

| Oracle/PL/SQL | PostgreSQL |
|---|---|
| `VARCHAR2` | `VARCHAR` veya `TEXT` |
| `NUMBER` | `INTEGER`, `NUMERIC`, `FLOAT` |
| `SYSDATE` | `NOW()` / `CURRENT_TIMESTAMP` |
| `NVL()` | `COALESCE()` |
| `ROWNUM` | `LIMIT` |
| `REFERENCES` | `REFERENCES` (aynı) |

SQL bilgisi %90 geçerli. İş mantığı veritabanında (stored procedure) değil Python'da yazılıyor — en büyük zihniyet farkı bu.

---

## SQLAlchemy — ORM Kavramı

**ORM (Object-Relational Mapper):** SQL'i Python nesnelerine çeviren katman.

PL/SQL'de:
```sql
INSERT INTO asset (isim, ip_adresi) VALUES ('web-server-01', '192.168.1.10');
SELECT * FROM asset WHERE id = 1;
```

SQLAlchemy ile:
```python
asset = Asset(isim="web-server-01", ip_adresi="192.168.1.10")
session.add(asset)
session.commit()

asset = db.query(Asset).filter(Asset.id == 1).first()
```

Arkada aynı SQL üretiliyor, biz yazmıyoruz.

**Neden ORM?**
- Tip güvenliği — sütun ismi yazım hatası mypy/IDE'de anında yakalanır
- Farklı veritabanları (PostgreSQL, SQLite) aynı kodla çalışır
- Karmaşık sorgularda direkt SQL de yazılabilir (`text()` ile)

**Karmaşık sorgular için:** JOIN, recursive CTE, window function gibi durumlarda ORM'i zorlamak yerine ham SQL yazılır:
```python
db.execute(text("SELECT ... FROM ... JOIN ... WHERE ..."))
```

---

## database.py — Kurulum

```python
from sqlalchemy import create_engine, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship
from datetime import datetime

DATABASE_URL = "postgresql://secflowx:secflowx123@localhost:5432/secflowx"
# Format: postgresql://kullanici:sifre@host:port/veritabani_adi
# PL/SQL'deki TNS/connection string karşılığı

engine = create_engine(DATABASE_URL)
# Bağlantıyı yöneten nesne — uygulama ayağa kalkarken bir kere oluşturulur
# PL/SQL'deki connection pool gibi

SessionLocal = sessionmaker(bind=engine)
# Her istek için ayrı session açan fabrika
# PL/SQL'deki transaction mantığı — aç, işle, commit/rollback, kapat

class Base(DeclarativeBase):
    pass
# Tüm tablo class'larının miras alacağı temel class
# SQLAlchemy "hangi class'lar tablo?" diye sorunca Base'e bakar
```

---

## Asset Modeli

```python
class Asset(Base):
    __tablename__ = "asset"   # veritabanındaki tablo adı

    id: Mapped[int] = mapped_column(primary_key=True)
    isim: Mapped[str] = mapped_column(String(100))
    ip_adresi: Mapped[str] = mapped_column(String(50), unique=True)
    olusturma_tarihi: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    bulgular: Mapped[list["Bulgu"]] = relationship(back_populates="asset")
```

PL/SQL karşılığı:
```sql
CREATE TABLE asset (
    id              NUMBER PRIMARY KEY,
    isim            VARCHAR2(100),
    ip_adresi       VARCHAR2(50) UNIQUE,
    olusturma_tarihi DATE DEFAULT SYSDATE
);
```

- `Mapped[int]` → sütun tipi
- `primary_key=True` → PK
- `unique=True` → UNIQUE constraint
- `default=datetime.utcnow` → PL/SQL'deki `DEFAULT SYSDATE`

---

## Bulgu Modeli ve Foreign Key

```python
class Bulgu(Base):
    __tablename__ = "bulgu"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    # ForeignKey("tablo_adi.sutun_adi") — PL/SQL'deki REFERENCES asset(id)
    cve: Mapped[str] = mapped_column(String(50))
    cvss_skoru: Mapped[float]
    aciklama: Mapped[str] = mapped_column(String(500))
    olusturma_tarihi: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["Asset"] = relationship(back_populates="bulgular")
```

PL/SQL karşılığı:
```sql
CREATE TABLE bulgu (
    id               NUMBER PRIMARY KEY,
    asset_id         NUMBER REFERENCES asset(id),
    cve              VARCHAR2(50),
    cvss_skoru       NUMBER,
    aciklama         VARCHAR2(500),
    olusturma_tarihi DATE DEFAULT SYSDATE
);
```

### relationship ve back_populates

SQL'de foreign key ilişkiyi tanımlar ama veriyi okumak için her seferinde JOIN yazman gerekir. `relationship` bu JOIN'i Python nesnesine taşır:

```python
# JOIN yazmadan asset'in tüm bulgularına erişim
asset = db.query(Asset).first()
asset.bulgular   # liste olarak gelir

# JOIN yazmadan bulgunun ait olduğu asset'e erişim
bulgu = db.query(Bulgu).first()
bulgu.asset      # Asset nesnesi olarak gelir
```

`back_populates` iki yönü birbirine bağlar:
- `Asset.bulgular` → o asset'e ait bulgu listesi
- `Bulgu.asset` → o bulgunun ait olduğu asset

---

## Alembic — Migration

PL/SQL'de şema değişikliği için DDL script'lerini elle yazardın. Alembic `database.py`'daki model değişikliklerini okuyup SQL'i **otomatik üretiyor**.

### Kurulum

```bash
pip install sqlalchemy alembic psycopg2-binary
alembic init migrations
```

`alembic.ini` dosyasında bağlantıyı ayarla:
```ini
sqlalchemy.url = postgresql://secflowx:secflowx123@localhost:5432/secflowx
```

`migrations/env.py` dosyasında modelleri tanıt:
```python
from database import Base
target_metadata = Base.metadata
```

### Migration Komutları

```bash
# Migration dosyası oluştur (Alembic modeli okuyup SQL üretir)
alembic revision --autogenerate -m "asset tablosu eklendi"

# Migration'ı veritabanına uygula
alembic upgrade head

# Geri al
alembic downgrade -1
```

Oluşturulan migration dosyası içinde:
- `upgrade()` → `CREATE TABLE` — migration uygulandığında çalışır
- `downgrade()` → `DROP TABLE` — geri alındığında çalışır

`alembic_version` tablosu → hangi migration'ın uygulandığını takip eder. PL/SQL'deki `schema_version` tablosu gibi.

---

## main.py — Veritabanı Entegrasyonu

### get_db — Session Dependency

```python
from sqlalchemy.orm import Session
from database import SessionLocal, Asset, Bulgu

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Her istek için session açar, iş bitince kapatır. `yield` ile context manager gibi davranır — `yield`'e kadar "aç", `finally` "kapat". `Depends(get_db)` ile endpoint'lere enjekte edilir.

### Endpoint'ler

```python
# Asset ekleme
class AssetEkleIstegi(BaseModel):
    isim: str
    ip_adresi: str

@app.post("/asset")
def asset_ekle(istek: AssetEkleIstegi, db: Session = Depends(get_db)):
    yeni_asset = Asset(isim=istek.isim, ip_adresi=istek.ip_adresi)
    db.add(yeni_asset)       # INSERT hazırla — PL/SQL'deki INSERT
    db.commit()              # veritabanına yaz — PL/SQL'deki COMMIT
    db.refresh(yeni_asset)   # DB'nin atadığı id/tarih gibi alanları geri yükle
    return {"id": yeni_asset.id, "isim": yeni_asset.isim, "ip_adresi": yeni_asset.ip_adresi}

# Asset listele
@app.get("/assets")
def asset_listele(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()   # SELECT * FROM asset
    return assets

# Bulgu ekleme
class BulguEkleIstegi(BaseModel):
    asset_id: int
    cve: str
    cvss_skoru: float
    aciklama: str

@app.post("/bulgu")
def bulgu_ekle(istek: BulguEkleIstegi, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == istek.asset_id).first()
    # .filter() → WHERE clause
    # .first() → ilk kaydı al, bulamazsa None döner (PL/SQL'deki ROWNUM = 1 gibi)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset bulunamadı")

    yeni_bulgu = Bulgu(
        asset_id=istek.asset_id,
        cve=istek.cve,
        cvss_skoru=istek.cvss_skoru,
        aciklama=istek.aciklama
    )
    db.add(yeni_bulgu)
    db.commit()
    db.refresh(yeni_bulgu)
    return yeni_bulgu

# Asset'e ait bulgular — relationship kullanımı
@app.get("/asset/{asset_id}/bulgular")
def asset_bulgulari(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset bulunamadı")
    return asset.bulgular   # relationship — JOIN yazmadan
```

### Sorgu Metotları

| SQLAlchemy | SQL karşılığı |
|---|---|
| `db.query(Asset).all()` | `SELECT * FROM asset` |
| `db.query(Asset).filter(Asset.id == 1).first()` | `SELECT * FROM asset WHERE id = 1 AND ROWNUM = 1` |
| `db.add(nesne)` + `db.commit()` | `INSERT ... ; COMMIT` |
| `asset.bulgular` | `SELECT * FROM bulgu WHERE asset_id = ?` (JOIN) |

---

## 🎯 Faz 1 — Hafta 1 Durumu: ✅ TAMAMLANDI

- [x] Modern Python syntax (type hints, dataclass, comprehension, context manager, exception handling)
- [x] `venv`, `pip`, `requirements.txt`
- [x] `ruff`, `mypy`
- [x] `asyncio` mantığı
- [x] `pyproject.toml` (kavramsal giriş)
- [x] `.gitignore` kullanımı

---

## 🎯 Faz 1 — Hafta 2 Durumu: ✅ TAMAMLANDI

- [x] FastAPI kurulum, uvicorn, /docs Swagger UI
- [x] Path parameter
- [x] Query parameter
- [x] Pydantic ile response modeli (BaseModel)
- [x] POST endpoint ve request body
- [x] HTTP hata kodları (400, 404, HTTPException)
- [x] Dependency injection
- [x] Kimlik doğrulama: JWT, OAuth2 password flow, RBAC
- [x] httpx ile dış servislere async istek (OSINT — ip-api.com)

---

## 🎯 Faz 1 — Hafta 3 Durumu: 🔄 DEVAM EDİYOR

- [x] PostgreSQL Docker ile kurulum
- [x] SQLAlchemy — ORM kavramı
- [x] `database.py` — engine, SessionLocal, Base
- [x] `Asset` modeli tanımlama
- [x] `Bulgu` modeli ve ForeignKey
- [x] `relationship` ve `back_populates`
- [x] Alembic — migration oluşturma ve uygulama
- [x] CRUD endpoint'leri veritabanıyla entegre etme
- [ ] pytest — unit test, fixture, API endpoint testi, mock
- [ ] Docker Compose — DB + app birlikte

*Bu döküman, Claude ile yapılan interaktif öğrenme oturumlarının özetidir. SecFlowX Ekibi Öğrenme Yol Haritası'nın Faz 0, Faz 1 Hafta 1, Hafta 2 ve Hafta 3 bölümlerini kapsar.*

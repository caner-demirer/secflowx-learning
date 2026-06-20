#--------------------------------------------------------------------------
# DEĞİŞKENLER VE TİPLER
#--------------------------------------------------------------------------
# aslında bir tip belirtme zorunluluğu yok ama daha analaşılır olması için belirtiyoruz
isim: str = "Caner"
yas: int = 35
aktif: bool = True
maas: float = 25000.50

#--------------------------------------------------------------------------
# KOLEKSIYONLAR
#--------------------------------------------------------------------------

#------------------------------------
#- List
#------------------------------------
# pl/sql de array
zafiyetler: list[str] = ["SQL Injection", "XSS", "SSRF"]
zafiyetler.append("CSRF")   # list e ekleme yaparken "append" set e ekleme yaparken "add" kullanılır
print(zafiyetler[0])        # "SQL Injection" — index 0'dan başlar!

#------------------------------------
#- Dict(key,value)
#------------------------------------
def tarama_yap(host: str, port: int) -> dict:           # -> işareti fonksiyonun ne döndüreceğini gösterir pl/sql de fonksiyon başında yazığımız "return number" gibi
    sonuc = {
        "host": host,
        "port": port,
        "durum": "açık" if port == 443 else "kapalı",   # "CASE WHEN port = 443 THEN 'açık' ELSE 'kapalı' END" gibi sadece tek dğer kontrolü yapılırsa kullanılıyor
        "servis": "https" if port == 443 else "bilinmiyor"
    }
    return sonuc

rapor = tarama_yap("192.168.1.10", 443)
print(rapor)            # {'host': '192.168.1.10', 'port': 443, 'durum': 'açık', 'servis': 'https'}
print(rapor["durum"])   # açık

#------------------------------------
#- Tuple -> değiştirilemez liste
#------------------------------------
koordinat: tuple[int, int] = (10, 20)

#------------------------------------
#- Set -> benzersiz elemnların bulunduğu liste pl/sql de distinct 
#------------------------------------
portlar: set[int] = {22, 80, 443, 443}  # tekrar eden 443 otomatik silinir

#--------------------------------------------------------------------------
# KONTROL YAPILARI
#--------------------------------------------------------------------------
# Python'da BEGIN/END yok, noktalı virgül yok. Blok, girintilemeyle (indentation) belirlenir. Bu en çok alışman gereken şey olacak — girinti yanlışsa kod çalışmaz.

#------------------------------------
#- If
#------------------------------------
if yas >= 18:
    print("Yetişkin")
elif yas >= 13:
    print("Genç")
else:
    print("Çocuk")

#------------------------------------
#- For
#------------------------------------
for i in range(1, 11):      # pl/sql de FOR i IN 1..10 LOOP
    print(i)

for zafiyet in zafiyetler:  # pl/sql de cursor döngüsü. zafiyet burda değişken for içine yazınca zafiyetler listesinin tipinde otomatik tanımlanıyor.
    print(zafiyet)

#------------------------------------
#- While
#------------------------------------
while sayac < 5:
    print(sayac)
    sayac += 1

#--------------------------------------------------------------------------
# FONKSIYONLAR
#--------------------------------------------------------------------------
def topla(a: int, b: int) -> int:
    return a + b

sonuc = topla(5, 3)

#--------------------------------------------------------------------------
# EXCEPTION HANDLING
#--------------------------------------------------------------------------
try:
    sonuc = 10 / 0
except ZeroDivisionError:            # spesisifk expetion pl/sql de "NO_DATA_FOUND" gibi
    print("Sıfıra bölme hatası")
except Exception as e:               # e değişkeninin içine yazdığın mesajı verir
    print(f"Beklenmeyen hata: {e}")
finally:                             # burası kod hata versede vermesde çalışan bölüm. Genelde Dosyayı kapatma veya başka temizlik işleri için en son çalıştırılıyor.
    print("Her durumda çalışır")

#--------------------------------------------------------------------------
# DATA CLASS
#--------------------------------------------------------------------------
# pl/sql de record type, dictin daha düzenlisi
from dataclasses import dataclass

@dataclass
class TaramaSonucu:
    host: str
    port: int
    durum: str

sonuc = TaramaSonucu(host="192.168.1.10", port=443, durum="açık")

print(sonuc.host)   # 192.168.1.10  (dict["host"] değil, sonuc.host!)
print(sonuc.port)   # 443

#--------------------------------------------------------------------------
# LIST/DICT COMPREHANSION
#--------------------------------------------------------------------------

#------------------------------------
#- List Comprehansion 
#------------------------------------
#For döngüsü ile liste oluşturma
sayilar = [1, 2, 3, 4, 5]
karesi = []

for sayi in sayilar:
    karesi.append(sayi ** 2)    # sayı üzeri 2 demek. 5 ** 3 => 5 üzeri 3 demek, 5x5x5

print(karesi)                   # [1, 4, 9, 16, 25]

#Comprehansion ile liste oluşturma
sayilar = [1, 2, 3, 4, 5]
karesi = [sayi ** 2 for sayi in sayilar]    #[ifade  for eleman  in liste]

print(karesi)                               # [1, 4, 9, 16, 25]

#Koşullu Comprehension (Filtreleme)
# Normal yöntem
acik_portlar = []
for port in portlar:
    if port in [80, 443]:
        acik_portlar.append(port)

# Comprehension ile
acik_portlar = [port for port in portlar if port in [80, 443]]  #[ifade for eleman in liste if koşul]

print(acik_portlar)   # [80, 443]

#------------------------------------
#- Dict Comprehansion 
#------------------------------------
#Basit, kısa dönüşümler için harika. Karmaşık mantık varsa (birden fazla if, nested loop) okunaklılık bozulur, normal for döngüsü daha iyi
cve_listesi = ["CVE-2024-1234", "CVE-2024-5678"]

# Her CVE'ye varsayılan bir skor ata
cve_skorlari = {cve: 0.0 for cve in cve_listesi}
print(cve_skorlari) # {'CVE-2024-1234': 0.0, 'CVE-2024-5678': 0.0} 

# Bu kadar basitse → comprehension güzel
kareler = [x**2 for x in sayilar]

# Bu kadar karmaşıksa → normal for döngüsü kullan
for x in sayilar:
    if x % 2 == 0:
        if x > 10:
            sonuc.append(x * 2)
        else:
            sonuc.append(x)

#--------------------------------------------------------------------------
# CONTEXT MANAGER (with STATEMENT)
#--------------------------------------------------------------------------
# dosya aç - işini yap - dosya kapat
# Tarama sonuçlarını dosyaya yazarken, veritabanı bağlantısı açarken, network bağlantısı kurarken kullanılır

#Yanlış/Eski Yöntem
dosya = open("rapor.txt")
veri = dosya.read()
dosya.close()           # bunu unutursan dosya açık kalır, sorun çıkarır

# with ile Doğru Yöntem
with open("rapor.txt") as dosya:
    veri = dosya.read() # buradan çıkınca dosya OTOMATİK kapanır, hata olsa bile
                        # with bloğu bitince (veya içinde hata çıksa bile) kaynağı otomatik temizler. Yani aslında bir nevi otomatik finally mantığı var içinde.

# Dosyaya tarama sonucu yazma
with open("tarama_sonucu.json", "w") as f:
    f.write(json.dumps(sonuc))

# Veritabanı bağlantısı
with db.session() as session:
    session.add(yeni_kayit)
    session.commit()

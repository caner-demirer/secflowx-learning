# SecFlowX Ekibi — Yeni Başlayan Öğrenme Yol Haritası

**Hedef:** Python backend, siber güvenlik temelleri ve tarama araçlarını, sonunda mini bir SPM (Security Posture Management) servisi kurabilecek seviyede öğrenmek.

**Süre:** ~12 hafta (haftada ~15-20 saat varsayımıyla). Kişinin önceki tecrübesine göre fazlar kısaltılabilir.

**Felsefe:** Üç alanı izole öğrenmek yerine birbirine bağlıyoruz. Python'ı "bir tarayıcıyı çalıştırıp çıktısını işleyen backend", güvenlik temellerini "neyi neden tarıyoruz" olarak öğreniyoruz. Her faz somut bir çıktıyla (pratik proje) bitiyor; teori tek başına yeterli sayılmıyor.

---

## Faz 0 — Kurulum ve Zihinsel Harita (3-4 gün)

Amaç: ortamı hazırlamak ve "SPM nedir, biz ne yapıyoruz" sorusuna net cevap verebilmek.

**Konular**
- Geliştirme ortamı: Linux (WSL2 yeterli), Git/GitHub, VS Code, Docker Desktop kurulumu.
- Komut satırı temelleri: dosya sistemi, izinler, pipe/redirect, `grep`, `curl`, `ssh`.
- SPM kavramı: kurumun güvenlik duruşunu sürekli görünür kılma; misconfiguration, asset envanteri, risk skorlama, uyumluluk kanıtı.
- CSPM / SSPM / DSPM / ASPM ayrımı ve SecFlowX'in bu spektrumdaki yeri.

**Çıktı:** Kendi cümleleriyle yazılmış yarım sayfalık "SPM ve SecFlowX ne işe yarar" notu (mentor ile gözden geçirilir).

---

## Faz 1 — Python Backend Temelleri (3 hafta)

Amaç: tip güvenli, async, test edilebilir bir API servisi yazabilmek. SecFlowX backend'i Python ise zaten günlük işin çekirdeği burası.

### Hafta 1 — Python core + araç zinciri
- Modern Python: type hints, `dataclass`, list/dict comprehension, context manager, exception handling.
- Ortam yönetimi: `venv`, `pip`, `pyproject.toml`, bağımlılık kilitleme.
- Kod kalitesi: `ruff` (lint + format), `mypy` (statik tip kontrolü).
- `asyncio` mantığı: event loop, `async/await`, eşzamanlı I/O neden önemli (tarayıcılar I/O-bound iştir).

### Hafta 2 — FastAPI ile API geliştirme
- FastAPI temelleri: path/query parametreleri, request/response modelleri.
- **Pydantic** ile veri doğrulama ve serialization (güvenlik ürününde girdi doğrulaması kritik).
- Bağımlılık enjeksiyonu (dependency injection), middleware, hata yönetimi.
- Kimlik doğrulama: JWT, OAuth2 password flow, rol bazlı yetkilendirme (RBAC).
- `httpx` ile dış servislere async istek (NVD/OSV API'leri vb.).

### Hafta 3 — Veri katmanı ve arka plan işleri
- **PostgreSQL** + **SQLAlchemy** (2.0 stili) + Alembic ile migration.
- Veri modelleme: asset, bulgu (finding), tarama (scan) ilişkileri.
- Uzun süren işler: tarama işlerini bloke etmeden çalıştırmak için Celery / RQ / APScheduler mantığı.
- `pytest` ile test: unit test, fixture, API endpoint testi, mock'lama.
- Docker: servisi container'a alma, `docker compose` ile DB + app birlikte ayağa kaldırma.

**Faz 1 projesi:** Basit bir "Asset Inventory API". CRUD endpoint'leri, Pydantic doğrulama, JWT auth, PostgreSQL kalıcılık, pytest testleri, Docker ile çalışan hali. → Bu, capstone projesinin iskeleti olacak.

**Tamamlanma kriteri:** Kişi sıfırdan tip güvenli, testli, container'da çalışan bir FastAPI servisi açıklayarak yazabiliyor.

---

## Faz 2 — Siber Güvenlik Temelleri (3 hafta)

Amaç: tarama sonuçlarını "anlamlandırabilmek". Bir CVE'nin neden kritik olduğunu, bir misconfiguration'ın neyi açtığını bilmeden iyi bir SPM backend yazılamaz.

### Hafta 4 — Temel güvenlik ve ağ
- CIA üçlüsü (gizlilik/bütünlük/erişilebilirlik), saldırı yüzeyi, tehdit modelleme (STRIDE'a giriş).
- Ağ temelleri: TCP/IP, portlar, DNS, HTTP/HTTPS, TLS el sıkışması, sertifikalar.
- Kimlik & kriptografi temeli: hashing vs. şifreleme, simetrik/asimetrik, parola saklama (bcrypt/argon2), secret yönetimi (Vault mantığı).

### Hafta 5 — Uygulama ve bulut güvenliği
- **OWASP Top 10**: injection, broken auth, SSRF, security misconfiguration vb. — her birini örnekle.
- API güvenliği (OWASP API Top 10): SecFlowX kendisi de bir API ürünü.
- Bulut güvenliği temelleri: IAM, en az ayrıcalık, açık S3/storage, yanlış güvenlik grubu — CSPM'in tam da yakaladığı şeyler.

### Hafta 6 — Zafiyet ekonomisi ve uyumluluk
- Zafiyet zinciri: **CVE → CVSS skoru → CWE → NVD / OSV** veri kaynakları. CVSS vektörünü okuyabilmek (örn. AV:N/AC:L...).
- Önceliklendirme: CVSS + EPSS + exploit varlığı + iş bağlamı ile gerçek risk skorlama.
- Uyumluluk çerçeveleri: **ISO/IEC 27001**, **CIS Benchmarks**, **NIST**, **PCI-DSS** ve Türkiye bağlamında **KVKK** + kamu/BTK gereksinimleri. SecFlowX müşterileri (PTT, Türksat, HAVELSAN, MSB, DHMI...) çoğunlukla bunlara mapping ve kanıt ister.

**Faz 2 projesi:** Bir örnek CVE seçip uçtan uca analizi: CVSS vektörünün açılımı, etkilenen bileşen, CIS/ISO hangi kontrolle ilişkili, bir kurumda nasıl önceliklendirilirdi. Tek sayfa rapor.

**Tamamlanma kriteri:** Kişi rastgele bir tarama bulgusuna bakıp "bu neden önemli, hangi standardı ihlal ediyor, önceliği ne" sorularını yanıtlayabiliyor.

---

## Faz 3 — Tarama Araçları (3 hafta)

Amaç: araçları sadece çalıştırmak değil; **çıktılarını programatik olarak işleyebilmek** (SARIF/JSON parse, normalize, skorla). SPM'in kalbi budur.

### Hafta 7 — Ağ ve zafiyet tarayıcıları
- **Nmap**: host keşfi, port/servis tespiti, NSE script'leri; çıktıyı XML/JSON alıp parse etme.
- **OpenVAS / Greenbone** (ve kavramsal olarak Nessus): network vulnerability scanning mantığı, tarama profilleri, false positive yönetimi.

### Hafta 8 — Container, bağımlılık ve secret tarama
- **Trivy** ve **Grype**: container imajı, OS paketleri ve bağımlılık zafiyetleri; JSON/SARIF çıktısı.
- Bağımlılık/SCA: **OSV-Scanner**, Python için `pip-audit` ve **Safety**; **OSV.dev** API'si.
- SAST: **Semgrep**, Python için **Bandit**.
- Secret tarama: **gitleaks**, **trufflehog**.
- IaC tarama: **Checkov**, **tfsec** (yanlış yapılandırmaları kodda yakalama).

### Hafta 9 — Web app tarama + çıktı standardizasyonu
- **OWASP ZAP**, **Nuclei**, Nikto ile web/uygulama taraması.
- Ortak çıktı formatları: **SARIF**, JSON şemaları; farklı araçların çıktısını **tek bir normalize edilmiş bulgu modeline** indirgeme.
- Bir tarayıcıyı Python'dan `subprocess` ile çalıştırıp çıktısını yakalama, parse etme, deduplike etme.

**Faz 3 projesi:** Python ile küçük bir "scanner wrapper": Trivy veya OSV-Scanner'ı çalıştırır, JSON çıktısını Pydantic modeline parse eder, CVSS'e göre sıralar, normalize edilmiş bulgu listesi döner.

**Tamamlanma kriteri:** Kişi en az iki tarayıcının çıktısını programatik olarak işleyip ortak modele dönüştürebiliyor.

---

## Faz 4 — Birleştirme: Mini SPM Servisi (Capstone, 2 hafta)

Amaç: üç alanı tek üründe birleştirmek. Bu proje SecFlowX'in çekirdek akışının küçük bir kopyasıdır ve kişinin gerçek işe hazır olduğunu gösterir.

### Hafta 10-11 — İnşa
FastAPI servisi olarak:
1. **Asset/hedef ekleme** endpoint'i (Faz 1 iskeleti üzerine).
2. **Tarama tetikleme**: seçilen bir tarayıcıyı (Trivy / OSV-Scanner / Nmap) arka plan işi olarak çalıştırma.
3. **Normalize etme**: çıktıyı ortak bulgu modeline dönüştürme.
4. **Risk skorlama**: CVSS + basit iş-bağlamı çarpanıyla önceliklendirme.
5. **Kalıcılık**: bulguları PostgreSQL'e yazma, geçmiş taramalarla karşılaştırma (yeni/çözülen bulgu).
6. **Sunum**: bulguları listeleyen ve özet skor veren bir API + basit dashboard.
7. **Uyumluluk eşlemesi (opsiyonel/bonus):** bulguları CIS/ISO kontrolleriyle ilişkilendirme.

### Hafta 12 — Sağlamlaştırma ve sunum
- Testler, hata yönetimi, Docker Compose ile tek komutla ayağa kaldırma.
- Kendi servisini kendi araçlarıyla tarama (Bandit + pip-audit) — "güvenlik ürünü güvenli mi" refleksi.
- Ekibe 20 dakikalık demo + mimari anlatımı.

**Tamamlanma kriteri:** Çalışan uçtan uca demo — hedef ekle → tara → normalize et → skorla → sun.

---

## Kalıcı Alışkanlıklar (tüm süre boyunca)

- **Her şeyi Git'e**: küçük commit'ler, anlamlı mesajlar, PR mantığı.
- **Okuma refleksi**: yeni bir CVE/teknik gördüğünde NVD veya OSV'den kaynağa gitme.
- **Resmi dokümantasyon önce**: FastAPI, Pydantic, Trivy, Nmap, OWASP gibi araçların kendi dokümanları birincil kaynak; blog/video ikincil.
- **Türkçe/İngilizce**: teknik terimleri İngilizce öğren, müşteriye/iç ekibe Türkçe anlatabilecek hale gel (presales/PoC bağlamı için kritik).

---

## Önerilen Birincil Kaynaklar (kategori bazında)

- **Python/FastAPI:** FastAPI resmi dokümanları (tutorial bölümü uçtan uca), Pydantic ve SQLAlchemy resmi dokümanları, `pytest` dokümantasyonu.
- **Güvenlik temelleri:** OWASP Top 10 ve OWASP API Top 10, OWASP Cheat Sheet Series; CIS Benchmarks dokümanları; NVD ve OSV.dev veri kaynakları.
- **Tarama araçları:** Trivy, Nmap, OWASP ZAP, Nuclei, gitleaks, Checkov resmi dokümanları (hepsi açık ve örnek-yoğun).
- **Sertifika hedefi (opsiyonel, motivasyon için):** Temel seviyede CompTIA Security+ müfredatı kavramsal çerçeveyi oturtmak için iyi bir kontrol listesi sağlar.

---

## Değerlendirme Noktaları (mentor için)

| Faz | Kontrol | Beklenen |
|-----|---------|----------|
| 1 | Mini API demo | Testli, container'da çalışan FastAPI servisi |
| 2 | CVE analiz raporu | CVSS okuma + uyumluluk ilişkilendirme |
| 3 | Scanner wrapper | İki aracın çıktısını normalize etme |
| 4 | Capstone demo | Uçtan uca tara→skorla→sun akışı |

> Not: Kişinin önceki Python/güvenlik tecrübesine göre Faz 1 veya Faz 2 kısaltılabilir; sıralama korunmalı çünkü her faz bir sonrakinin ön koşulu.

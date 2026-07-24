# python:3.11 -> Başlangıç noktası — Python 3.11 kurulu hazır bir Linux imajı
# -slim -> gereksiz paketler olmadan, küçük boyutlu. 
# Sıfırdan işletim sistemi kurmak yerine hazır imajdan başlıyoruz.
FROM python:3.11-slim

#Container içinde çalışma klasörü. Bundan sonraki tüm komutlar /app içinde çalışır.
WORKDIR /app

# Önce requirements.txt'i kopyala, sonra paketleri kur.
# Docker her satırı cache'liyor — kod değişse bile paketler yeniden kurulmaz, sadece requirements.txt değişince yeniden kurar. Hız için.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Tüm proje dosyalarını container'a kopyala.
COPY . .

# Container başlayınca çalışacak komut. --host 0.0.0.0 — dışarıdan erişime izin ver. Sadece localhost yazarsak container dışından erişemeyiz.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  
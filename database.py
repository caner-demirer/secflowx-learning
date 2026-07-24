from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://secflowx:secflowx123@localhost:5432/secflowx" #plsqldeki tns names

engine = create_engine(DATABASE_URL) # dbms_connection
SessionLocal = sessionmaker(bind=engine) # session

class Base(DeclarativeBase): # Şu an boş ama önemli. Bundan sonra tanımlayacağımız tüm tablolar bu Base'den miras alacak. SQLAlchemy "hangi class'lar tablo?" diye sorunca Base'e bakar.
    pass

class Asset(Base): # asset tablosu
    __tablename__ = "asset"

    # mapped ve mapped_column python syntaxı 
    id: Mapped[int] = mapped_column(primary_key=True)
    isim: Mapped[str] = mapped_column(String(100))
    ip_adresi: Mapped[str] = mapped_column(String(50), unique=True)
    olusturma_tarihi: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    bulgular: Mapped[list["Bulgu"]] = relationship(back_populates="asset") # iki tablo arasındaki relation ı tabloya tanımlıyoruz. SQLde selectte yazılan joini burda tanımlıyoruz.

# back_populates iki class'a ilişkinin iki yönünü da tanımlıyor.
# asset.bulgular  # bu asset'e ait tüm bulgular
# bulgu.asset  # bu bulgunun ait olduğu asset

class Bulgu(Base): # bulgu tablosu
    __tablename__ = "bulgu"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id")) # asset tablosundaki id alanına refere ediyor.
    cve: Mapped[str] = mapped_column(String(50))
    cvss_skoru: Mapped[float]
    aciklama: Mapped[str] = mapped_column(String(500))
    olusturma_tarihi: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    asset: Mapped["Asset"] = relationship(back_populates="bulgular")  # iki tablo arasındaki relation ı tabloya tanımlıyoruz. SQLde selectte yazılan joini burda tanımlıyoruz.


# TestClient -> Uvicorn'u başlatmadan, tarayıcı açmadan API'ye istek atan test istemcisi. 
# pytest bir dosyadaki test_ ile başlayan her fonksiyonu otomatik bulup çalıştırır. İsim test_ ile başlamak zorunda, yoksa görmez.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)   # test başında tabloları oluştur

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db  # main.py deki get_db yi override edip test için kullanılan db veriliyor.yani ana databasei değil test dbsini kullan demek.
    yield TestClient(app)                   # client'ı teste ver, test çalışsın
    Base.metadata.drop_all(bind=engine)     # test bitince tabloları sil

def test_root(client): 
    response = client.get("/")
    assert response.status_code == 200 # assert -> "Bu doğru olmalı" demek. Yanlışsa test hata verir.
    assert response.json() == {"mesaj": "SecFlowX API çalışıyor!"}

def test_asset_ekle(client):
    response = client.post("/asset", json={
        "isim": "test-server",
        "ip_adresi": "10.0.0.99"
    })
    assert response.status_code == 200
    assert response.json()["isim"] == "test-server"
    assert response.json()["ip_adresi"] == "10.0.0.99"
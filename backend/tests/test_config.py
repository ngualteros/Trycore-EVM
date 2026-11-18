from app.config import Settings


def test_database_url_from_environment(monkeypatch):
    url = "postgresql+psycopg://user:password@localhost:5432/test_db"
    monkeypatch.setenv("DATABASE_URL", url)

    assert Settings(_env_file=None).database_url == url

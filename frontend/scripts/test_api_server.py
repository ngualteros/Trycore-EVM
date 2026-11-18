import sys
import threading
import time
from pathlib import Path
from uuid import uuid4

BACKEND = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(BACKEND))

import uvicorn  # noqa: E402
from dotenv import dotenv_values  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.engine import make_url  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.db import get_session  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402


def main():
    value = dotenv_values(BACKEND / ".env.test").get("TEST_DATABASE_URL")
    if not value:
        raise SystemExit("Configure backend/.env.test first")
    url = make_url(value)
    if url.database != "trycore_evm_test" or url.drivername != "postgresql+psycopg":
        raise SystemExit("Only postgresql+psycopg and trycore_evm_test are allowed")
    schema = f"evm_frontend_{uuid4().hex}"
    engine = create_engine(url, hide_parameters=True, connect_args={"connect_timeout": 5})
    scoped = None
    created = False
    try:
        with engine.begin() as connection:
            assert connection.scalar(text("SELECT current_database()")) == "trycore_evm_test"
            connection.exec_driver_sql(f'CREATE SCHEMA "{schema}"')
        created = True
        scoped = create_engine(url, hide_parameters=True, connect_args={
            "connect_timeout": 5, "options": f"-csearch_path={schema}",
        })
        Base.metadata.create_all(scoped)

        def isolated_session():
            with Session(scoped, expire_on_commit=False) as session:
                yield session

        app.dependency_overrides[get_session] = isolated_session
        server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=18001, log_level="error"))
        thread = threading.Thread(target=server.run)
        thread.start()
        try:
            for _ in range(100):
                if server.started:
                    break
                if not thread.is_alive():
                    raise RuntimeError("API server did not start")
                time.sleep(0.05)
            if not server.started:
                raise RuntimeError("API server startup timed out")
            print("READY: isolated test API at http://127.0.0.1:18001; press Enter to stop and clean up", flush=True)
            sys.stdin.readline()
        finally:
            server.should_exit = True
            thread.join(timeout=15)
            if thread.is_alive():
                raise RuntimeError("API server did not stop")
    finally:
        app.dependency_overrides.pop(get_session, None)
        if scoped is not None:
            scoped.dispose()
        if created:
            # Only the random schema created by this invocation is eligible for cleanup.
            with engine.begin() as connection:
                connection.exec_driver_sql(f'DROP SCHEMA "{schema}" CASCADE')
            print("CLEANED: temporary frontend schema removed", flush=True)
        engine.dispose()


if __name__ == "__main__":
    main()

import time
import os
import sqlalchemy

def wait_for_db(db_url, retries=6, timeout=15):
    """Wait for the database to be available.

    :param db_url: the database URL
    :param timeout: the maximum number of seconds to wait
    """
    engine = sqlalchemy.create_engine(db_url, connect_args={'connect_timeout': 30})
    for i in range(retries):
        try:
            engine.connect()
            return
        except sqlalchemy.exc.OperationalError:
            print(f"Waiting for the database to be available ({i+1}/{retries})")
            time.sleep(timeout)
    raise RuntimeError("Timeout waiting for the database")

if __name__ == "__main__":
    # Get SQLIALCHEMY_DATABASE_URI from the environment
    db_url = os.environ["SQLALCHEMY_DATABASE_URI"]
    wait_for_db(db_url)
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://superset_user:Superset123!@localhost:5432/fleetstat"

engine = create_engine(DATABASE_URL)

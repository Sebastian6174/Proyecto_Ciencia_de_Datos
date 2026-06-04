from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/fast_and_safe_dw"
)

conn = engine.connect()

print("Conexión exitosa")

conn.close()
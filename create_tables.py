from app.db import Base, engine
import app.models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")

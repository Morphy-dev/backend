from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth  # Ensure you have an `auth.py` file inside `app/routes/`

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

from app.routes import schools

app.include_router(schools.router, tags=["schools"])

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "FastAPI Backend is Running"}

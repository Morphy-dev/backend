from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth  # Ensure you have an `auth.py` file inside `app/routes/`
from fastapi.middleware.cors import CORSMiddleware
from app.routes.Groups import groups
from app.routes import schools
from app.routes.Lessons import lessons

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods
    allow_headers=["*"],  # ✅ Allow all headers
)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


app.include_router(schools.router, tags=["schools"])

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])


app.include_router(groups.router, prefix='/groups', tags=["groups"])


app.include_router(lessons.router, prefix='/lessons', tags=["lessons"])

print(app.routes)
@app.get("/")
def root():
    return {"message": "FastAPI Backend is Running"}

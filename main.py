from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from utils.database import engine, Base
from routes import orders
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")

    # Yield control back to FastAPI
    yield

    # Shutdown code
    print("Application shutdown.")


app = FastAPI(
    title="Bullscatch API",
    description="API for the Bullscatch App",
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)



allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",

]

app.include_router(
    orders.router,
    prefix="/orders",
    tags=["orders"],
    include_in_schema=True,
)

@app.get(
    "/",
    summary="Root endpoint",
    description="The root endpoint serves as a welcome page for the Bullscatch App.",
)
def root():
    return {"message": "Welcome to the Paper trading Broker"}
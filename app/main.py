from fastapi import FastAPI

app = FastAPI(
    title="Book AI API",
    description="API para recomendar libros basados en series de TV usando IA",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "¡Hola Simón! Tu API de libros está funcionando 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API corriendo correctamente"}
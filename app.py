from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import random
import uvicorn
from typing import Dict, Any
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Coin Flip API",
    description="Простое API для подбрасывания монетки",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница с веб-интерфейсом"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api")
async def api_info():
    """API информация"""
    return {
        "message": "Coin Flip API",
        "version": "1.0.0",
        "endpoints": {
            "flip": "/flip",
            "flip_multiple": "/flip/{count}",
            "health": "/health"
        }
    }

@app.get("/flip")
async def flip_coin() -> Dict[str, Any]:
    """Подбросить монетку один раз"""
    try:
        result = random.choice(["орел", "решка"])
        logger.info(f"Монетка подброшена: {result}")
        return {
            "result": result,
            "message": f"Выпал: {result}"
        }
    except Exception as e:
        logger.error(f"Ошибка при подбрасывании монетки: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/flip/{count}")
async def flip_multiple_coins(count: int) -> Dict[str, Any]:
    """Подбросить монетку несколько раз"""
    if count <= 0:
        raise HTTPException(status_code=400, detail="Количество должно быть больше 0")
    if count > 100:
        raise HTTPException(status_code=400, detail="Максимальное количество подбрасываний: 100")
    
    try:
        results = [random.choice(["орел", "решка"]) for _ in range(count)]
        heads_count = results.count("орел")
        tails_count = results.count("решка")
        
        logger.info(f"Подброшено {count} монеток: орлов - {heads_count}, решек - {tails_count}")
        
        return {
            "results": results,
            "summary": {
                "total": count,
                "heads": heads_count,
                "tails": tails_count
            },
            "message": f"Подброшено {count} монеток"
        }
    except Exception as e:
        logger.error(f"Ошибка при множественном подбрасывании: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Проверка состояния API"""
    return {"status": "healthy", "message": "API работает нормально"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
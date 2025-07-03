from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from databases import Database
import random
import uvicorn
from typing import Dict, Any, Optional
import logging
import os
import uuid
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к базе данных через переменные окружения
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://username:password@localhost:5432/database"
)

database = Database(DATABASE_URL)

app = FastAPI(
    title="Coin Flip API",
    description="Простое API для подбрасывания монетки с сохранением статистики",
    version="2.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("Подключение к базе данных установлено")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Подключение к базе данных закрыто")

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
        "message": "Coin Flip API с базой данных",
        "version": "2.0.0",
        "endpoints": {
            "flip": "/flip",
            "flip_multiple": "/flip/{count}",
            "stats": "/stats",
            "health": "/health"
        }
    }

async def save_flip_result(result: str, session_id: str, user_ip: str, user_id: Optional[int] = None):
    """Сохранить результат броска в базу данных"""
    query = """
    INSERT INTO coin_flips (user_id, result, session_id, user_ip)
    VALUES (:user_id, :result, :session_id, :user_ip)
    RETURNING id
    """
    values = {
        "user_id": user_id,
        "result": result,
        "session_id": session_id,
        "user_ip": user_ip
    }
    return await database.fetch_one(query, values)

@app.get("/flip")
async def flip_coin(request: Request) -> Dict[str, Any]:
    """Подбросить монетку один раз"""
    try:
        result = random.choice(["орел", "решка"])
        session_id = str(uuid.uuid4())
        user_ip = request.client.host
        
        # Сохраняем результат в базу данных
        saved_record = await save_flip_result(result, session_id, user_ip)
        
        logger.info(f"Монетка подброшена: {result}, ID записи: {saved_record['id']}")
        
        return {
            "result": result,
            "message": f"Выпал: {result}",
            "id": saved_record["id"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Ошибка при подбрасывании монетки: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/flip/{count}")
async def flip_multiple_coins(count: int, request: Request) -> Dict[str, Any]:
    """Подбросить монетку несколько раз"""
    if count <= 0:
        raise HTTPException(status_code=400, detail="Количество должно быть больше 0")
    if count > 100:
        raise HTTPException(status_code=400, detail="Максимальное количество подбрасываний: 100")
    
    try:
        results = []
        session_id = str(uuid.uuid4())
        user_ip = request.client.host
        saved_ids = []
        
        for _ in range(count):
            result = random.choice(["орел", "решка"])
            results.append(result)
            
            # Сохраняем каждый бросок
            saved_record = await save_flip_result(result, session_id, user_ip)
            saved_ids.append(saved_record["id"])
        
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
            "message": f"Подброшено {count} монеток",
            "saved_ids": saved_ids,
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"Ошибка при множественном подбрасывании: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/stats")
async def get_statistics() -> Dict[str, Any]:
    """Получить общую статистику бросков"""
    try:
        # Общая статистика
        total_query = "SELECT COUNT(*) as total FROM coin_flips"
        total_result = await database.fetch_one(total_query)
        
        # Статистика по результатам
        stats_query = """
        SELECT 
            result,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM coin_flips), 2) as percentage
        FROM coin_flips 
        GROUP BY result
        """
        stats_result = await database.fetch_all(stats_query)
        
        # Последние 10 бросков
        recent_query = """
        SELECT result, timestamp 
        FROM coin_flips 
        ORDER BY timestamp DESC 
        LIMIT 10
        """
        recent_result = await database.fetch_all(recent_query)
        
        return {
            "total_flips": total_result["total"],
            "results_breakdown": [dict(row) for row in stats_result],
            "recent_flips": [dict(row) for row in recent_result]
        }
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения статистики")

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Проверка состояния API и базы данных"""
    try:
        # Проверяем подключение к базе данных
        await database.fetch_one("SELECT 1")
        return {
            "status": "healthy", 
            "message": "API и база данных работают нормально",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Ошибка проверки здоровья: {e}")
        return {
            "status": "unhealthy", 
            "message": "Проблемы с базой данных",
            "database": "disconnected"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
# 🪙 Coin Flip API

Современное веб-приложение для подбрасывания монетки с базой данных PostgreSQL, построенное на FastAPI и Docker.

## ✨ Возможности

- 🎯 **Подбрасывание монетки** - одиночные и множественные броски
- 🗄️ **База данных PostgreSQL** - сохранение всех результатов
- 📊 **Статистика в реальном времени** - анализ всех бросков
- 🌐 **Красивый веб-интерфейс** - интуитивно понятный дизайн
- 🐳 **Docker контейнеризация** - легкое развертывание
- 📱 **Адаптивный дизайн** - работает на всех устройствах
- 🔍 **Аналитика** - отслеживание сессий и IP адресов

## 🚀 Быстрый старт

### Запуск с Docker

```bash
# Клонировать репозиторий
git clone https://github.com/Svetarik221/coin-flip-api.git
cd coin-flip-api

# Собрать образ
docker build -t coin-flip-api .

# Запустить контейнер
docker run -d --name coin-flip-api -p 8000:8000 coin-flip-api
```

### Запуск с Docker Compose

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: `http://localhost:8000`

## 📚 API Документация

### Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/` | Веб-интерфейс |
| `GET` | `/flip` | Подбросить монетку один раз |
| `GET` | `/flip/{count}` | Подбросить монетку {count} раз |
| `GET` | `/stats` | Получить статистику всех бросков |
| `GET` | `/health` | Проверить состояние API и БД |

### Примеры использования

**Одиночный бросок:**
```bash
curl http://localhost:8000/flip
```
```json
{
  "result": "орел",
  "message": "Выпал: орел", 
  "id": 1,
  "timestamp": "2025-07-03T19:18:40.161054"
}
```

**Множественные броски:**
```bash
curl http://localhost:8000/flip/5
```
```json
{
  "results": ["решка", "орел", "решка", "решка", "орел"],
  "summary": {
    "total": 5,
    "heads": 2,
    "tails": 3
  },
  "message": "Подброшено 5 монеток",
  "saved_ids": [2, 3, 4, 5, 6],
  "session_id": "5ff25b91-8003-4dac-9743-99cfc7998ac5"
}
```

**Статистика:**
```bash
curl http://localhost:8000/stats
```
```json
{
  "total_flips": 6,
  "results_breakdown": [
    {"result": "орел", "count": 3, "percentage": "50.00"},
    {"result": "решка", "count": 3, "percentage": "50.00"}
  ],
  "recent_flips": [
    {"result": "орел", "timestamp": "2025-07-03T19:18:52.956748"},
    {"result": "решка", "timestamp": "2025-07-03T19:18:52.823904"}
  ]
}
```

## 🗄️ База данных

Приложение использует PostgreSQL для хранения статистики бросков.

### Структура таблицы `coin_flips`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | SERIAL PRIMARY KEY | Уникальный идентификатор |
| `user_id` | INTEGER | Связь с пользователем (опционально) |
| `result` | VARCHAR(10) | Результат броска ("орел"/"решка") |
| `timestamp` | TIMESTAMP | Время броска |
| `session_id` | VARCHAR(50) | Идентификатор сессии |
| `user_ip` | VARCHAR(45) | IP адрес пользователя |

### Настройка базы данных

1. **Создать PostgreSQL базу данных**
2. **Обновить подключение** в `app.py`:
```python
DATABASE_URL = "postgresql://username:password@host:port/database"
```
3. **Таблица создается автоматически** при первом запуске

## 🛠️ Технологии

- **Backend:** FastAPI (Python 3.11)
- **База данных:** PostgreSQL
- **ORM:** databases + asyncpg
- **Контейнеризация:** Docker & Docker Compose
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Стилизация:** Градиенты, анимации, адаптивный дизайн

## 📁 Структура проекта

```
coin-flip-api/
├── app.py                 # Основное FastAPI приложение
├── requirements.txt       # Python зависимости
├── Dockerfile            # Docker образ для API
├── Dockerfile.frontend   # Docker образ для frontend
├── docker-compose.yml    # Оркестрация контейнеров
├── templates/
│   └── index.html        # Веб-интерфейс
├── coin-flip-frontend.html # Автономный frontend
├── business-improvements.md # План развития
└── README.md            # Документация
```

## 🚀 Развертывание в продакшене

### 1. Настройка переменных окружения

```bash
export DATABASE_URL="postgresql://user:pass@host:port/db"
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

### 2. Использование Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
```

### 3. Мониторинг

Проверка состояния:
```bash
curl http://your-domain.com/health
```

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 👨‍💻 Автор

**Svetlana Vostrecova** ([@Svetarik221](https://github.com/Svetarik221))

## 🙏 Благодарности

- FastAPI за отличную документацию
- PostgreSQL за надежную базу данных
- Docker за упрощение развертывания

---

⭐ **Понравился проект? Поставьте звездочку!** ⭐ 
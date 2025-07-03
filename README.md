# Coin Flip API

Простое API для подбрасывания монетки, созданное с использованием FastAPI и Docker.

## Возможности

- Подбросить монетку один раз
- Подбросить монетку несколько раз (до 100)
- Проверка состояния API
- Автоматическая документация API

## Запуск с Docker

### Способ 1: Docker Compose (рекомендуется)

```bash
# Собрать и запустить контейнер
docker-compose up --build

# Запустить в фоновом режиме
docker-compose up -d --build

# Остановить
docker-compose down
```

### Способ 2: Docker напрямую

```bash
# Собрать образ
docker build -t coin-flip-api .

# Запустить контейнер
docker run -p 8000:8000 coin-flip-api
```

## Использование API

После запуска API будет доступно по адресу `http://localhost:8000`

### Эндпоинты:

1. **GET /** - Информация об API
2. **GET /flip** - Подбросить монетку один раз
3. **GET /flip/{count}** - Подбросить монетку несколько раз
4. **GET /health** - Проверка состояния

### Примеры запросов:

```bash
# Подбросить монетку
curl http://localhost:8000/flip

# Подбросить 5 монеток
curl http://localhost:8000/flip/5

# Проверить состояние
curl http://localhost:8000/health
```

## Документация API

После запуска доступна автоматическая документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Возможные проблемы и решения

### 1. Порт 8000 занят
Если порт 8000 уже используется, измените порт в `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Используйте другой порт
```

### 2. Проблемы с правами доступа
```bash
# На Linux/Mac может потребоваться
sudo docker-compose up --build
```

### 3. Проблемы с сетью
```bash
# Проверьте, что Docker запущен
docker --version

# Проверьте статус контейнера
docker ps
```

## Разработка

Для локальной разработки без Docker:

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
python app.py
``` 
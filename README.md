
---

## Архитектура проекта

### Структура проекта

```
app/
│
├── ai/                         # AI-модуль
│   └── lead_ai_service.py
│
├── api/                        # HTTP-слой (роутеры)
│   └── v1/
│       ├── leads.py            # Эндпоинты для работы с лидами
│       └── sales.py            # Эндпоинты для работы с продажами
│
├── core/                       # Общие компоненты
│   ├── config.py               # Конфигурация приложения
│   └── exceptions.py           # Кастомные исключения
│
├── db/                         # Работа с базой данных
│   ├── models/
│   │   ├── lead.py             # SQLAlchemy модель Lead
│   │   └── sale.py             # SQLAlchemy модель Sale
│   │
│   └── session.py              # Async session
│
├── main.py                     # Точка входа, инициализация FastAPI
│
├── repositories/               # Слой доступа к данным
│   ├── lead_repository.py
│   └── sale_repository.py
│
├── schemas/                    # Pydantic-схемы
│   ├── ai.py
│   ├── lead.py
│   └── sale.py
│
└── services/                   # Бизнес-логика
    ├── lead_service.py
    └── sale_service.py
    
requirements.txt            # Зависимости проекта
README.md                       # Документация проекта
```

---

## Логическая архитектура

Система разделена на несколько уровней ответственности.

### API Layer
- Принимает HTTP-запросы  
- Валидирует входные данные через Pydantic  
- Передает управление в сервисный слой  
- Не содержит бизнес-логики  

### Service Layer
Основной слой бизнес-логики:
- управление этапами лида  
- контроль переходов между стадиями  
- проверка условий передачи в продажи  
- взаимодействие с AI-модулем  

### Repository Layer
- Изолирует работу с PostgreSQL  
- Использует async SQLAlchemy  
- Не содержит бизнес-правил  

### AI Layer
AI-модуль:
- анализирует данные лида  
- рассчитывает вероятность сделки (score)  
- возвращает рекомендацию  

AI не изменяет данные напрямую — окончательное решение принимает бизнес-логика.

---

## Поток обработки лида

```
Lead created

Cold stages (new → contacted → qualified → transferred → lost)

AI analysis

Decision (transfer or not)

Sales pipeline (new → kyc → agreement → paid → lost)
```

---

## Технологии

- Python 3.11+
- FastAPI (async)
- PostgreSQL
- SQLAlchemy 2.0 (async)
- Pydantic

---
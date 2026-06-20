---
name: vector-push
description: "Load when setting up push notifications or alerting for any Vector ecosystem project. Self-hosted ntfy-based notification channel: one HTTP POST → push to all devices. No cloud, no registration."
---

# Vector Push — система уведомлений экосистемы Vector

Self-hosted push-уведомления через ntfy. Один HTTP POST → уведомление на всех устройствах. Без облака, без регистрации, без привязки к мессенджеру.

## Установка ntfy

```bash
# Docker (рекомендуется)
docker run -d --name ntfy -p 8080:80 binwiederhier/ntfy

# Или apt
sudo apt install ntfy
```

Приложение на телефон: [ntfy.sh](https://ntfy.sh) → подписаться на топик `http://<ваш-сервер>:8080/vector`

## Базовое использование

```bash
# Простое уведомление
curl -d "Конвейер остановлен — Цех №3" http://localhost:8080/vector

# С приоритетом и тегами
curl -H "Priority: high" -H "Tags: warning,rotating_light" \
     -d "Авария холодильника! Температура +8°C в камере №2" \
     http://localhost:8080/vector

# С заголовком
curl -H "Title: Меркурий — блокировка" \
     -d "Партия №456 заблокирована. Требуется ручная проверка эВСД." \
     http://localhost:8080/vector
```

## Приоритеты

| Priority | Поведение | Для чего |
|----------|----------|---------|
| `max` | Звук + вибрация + всплывающее окно, даже в беззвучном | Авария, пожар, остановка производства |
| `high` | Звук + вибрация | Критическая ошибка, блокировка партии |
| `default` | Обычное уведомление | Завершение задачи, отчёт готов |
| `low` | Без звука | Информационное: ежедневный брифинг |
| `min` | Только в шторке уведомлений | Фоновое: бэкап завершён |

## Топики для экосистемы Vector

| Топик | Проект | Что уведомляет |
|-------|--------|---------------|
| `vector-meat-critical` | Vector Meat | Остановка конвейера, авария холода, пожар, просрочка сырья |
| `vector-meat-mercury` | Vector Meat | Блокировка эВСД, ошибка Честного Знака |
| `vector-meat-haccp` | Vector Meat | Нарушение температурного режима, срыв санитарных норм |
| `vector-home-alarm` | Vector Home | Тревога, протечка, дым, датчик CO |
| `vector-home-presence` | Vector Home | Неожиданное движение, входная дверь без ключа |
| `vector-marketing-deals` | Vector Marketing | Сделка закрыта, клиент ответил, дедлайн |
| `vector-marketing-reports` | Vector Marketing | Отчёт готов, презентация сгенерирована |
| `vector-work-tasks` | Vector Work | Просроченная задача, ежедневный брифинг |
| `vector-legal-deadlines` | Vector Legal | Срок подачи иска, продление патента, изменение в реестре |
| `vector-system` | Все проекты | Бэкап завершён, сервер перегружен, диск заполнен |

## Сценарии применения

### Vector Meat — завод

```bash
# Критическое: авария холода
curl -H "Priority: max" -H "Tags: warning,rotating_light" \
     -H "Title: АВАРИЯ ХОЛОДИЛЬНИКА" \
     -d "Камера №2: t +8°C (норма 0..+4). Время сбоя: 14:32. Немедленно эвакуировать продукцию." \
     http://ntfy/vector-meat-critical

# Предупреждение: приближение к порогу
curl -H "Priority: high" -H "Tags: thermometer" \
     -H "Title: Камера №2 — на границе" \
     -d "Температура +3.8°C (порог +4.0). Проверить компрессор. Автоматическое ТО запланировано." \
     http://ntfy/vector-meat-haccp

# Информационное: смена завершена
curl -H "Priority: low" -H "Tags: white_check_mark" \
     -H "Title: Смена 14:00–22:00 завершена" \
     -d "Обвалено: 2.4 т. Фасовка: 1.8 т. Отгрузка: 3 партии. Брак: 0.3%." \
     http://ntfy/vector-meat-critical
```

### Vector Marketing — клиентские уведомления

```bash
# Сделка закрыта
curl -H "Priority: high" -H "Tags: moneybag,tada" \
     -H "Title: Сделка закрыта — Яндекс.Лавка" \
     -d "Контракт на SEO-продвижение подписан. Сумма: 450 000 ₽/мес. Старт: 1 июня." \
     http://ntfy/vector-marketing-deals

# Дедлайн через 1 час
curl -H "Priority: high" -H "Tags: alarm_clock" \
     -H "Title: Дедлайн через 1 час" \
     -d "Презентация для Озона. Осталось: 3 слайда. Ответственный: presentation-агент." \
     http://ntfy/vector-marketing-deals
```

### Vector Home — безопасность

```bash
# Тревога: движение при отсутствии
curl -H "Priority: max" -H "Tags: rotating_light,door" \
     -H "Title: ДВИЖЕНИЕ В ДОМЕ" \
     -d "Обнаружено движение в гостиной. Режим: НИКОГО НЕТ. Время: 23:15. Камера: включена." \
     http://ntfy/vector-home-alarm

# Информационное: пришёл домой
curl -H "Priority: low" -H "Tags: house" \
     -d "Дома. Температура 22°C. Свет в гостиной включён." \
     http://ntfy/vector-home-presence
```

### Vector Legal — контроль сроков

```bash
# Срок подачи иска
curl -H "Priority: high" -H "Tags: calendar,scales" \
     -H "Title: Срок подачи иска — завтра" \
     -d "Дело №А40-123/2026. Последний день подачи: 1 июня. Статус: проект готов, требуется финальная проверка." \
     http://ntfy/vector-legal-deadlines
```

## Интеграция с Hermes

```bash
# Через терминал
hermes "отправь ntfy-уведомление: конвейер остановлен, priority=high"

# Через cron
hermes cron create "every hour" --prompt "Проверь температуру в камерах. Если >+4°C — ntfy vector-meat-haccp priority=max"

# Через агентов
# Каждый агент Vector может отправлять уведомления через terminal:
# terminal: curl -H "Priority: high" -d "текст" http://ntfy/vector-топик
```

## Настройка на телефоне

1. Установить [ntfy Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) или [ntfy iOS](https://apps.apple.com/app/ntfy/id1625396347)
2. Добавить сервер: Settings → Add server → `http://<ваш-IP>:8080`
3. Подписаться на топики: `vector-meat-critical`, `vector-home-alarm`, `vector-marketing-deals`, `vector-work-tasks`

## Источник

- Hermes Agent ntfy docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/ntfy
- ntfy.sh: https://ntfy.sh — open-source, self-hosted push-уведомления

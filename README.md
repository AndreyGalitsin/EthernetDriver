# Ethernet Driver for Raspberry Pi and PC

Этот проект представляет собой реализацию драйвера для передачи данных по сети Ethernet между компьютером (PC) и Raspberry Pi с использованием модуля HR911105A (Ethernet PHY). Драйверы реализованы для двух устройств: Raspberry Pi и ПК, которые обмениваются JSON-данными.

## Описание

Проект включает два драйвера:

1. **Драйвер для Raspberry Pi (EthernetRPB)**:
    - Обеспечивает настройку GPIO пинов для взаимодействия с модулем HR911105A.
    - Настроен на прием и отправку данных по Ethernet.
    - Использует два потока: один для прослушивания входящих данных (`listener`), второй для отправки данных (`sender`).

2. **Драйвер для ПК (EthernetPC)**:
    - Настроен на прием и отправку данных по Ethernet.
    - Использует два потока: один для прослушивания входящих данных (`listener`), второй для отправки данных (`sender`).


## Настройка и подключение

### Установка и настройка на Raspberry Pi

1. Подключите модуль **HR911105A** к Raspberry Pi через GPIO пины, используя схемы подключения, указанные ниже.
### Схема подключения GPIO пинов

Для работы с Ethernet через HR911105A, на Raspberry Pi используются следующие пины:

| GPIO Pin | Подключение к модулю HR911105A        | 
|----------|----------------|
| 14       | TX1 (передача) | 
| 15       | TX-EN (управление передачей) |
| 18       | RX0 (прием)    |
| 24       | nINT/RETCLK    |
| 23       | TX0 (передача) |
| 25       | RX1 (прием)    |
| 8        | CRS (канал)    |
| 11       | MDC (управление) |
| 9        | MD10 (управление) |

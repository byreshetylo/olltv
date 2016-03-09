# olltv script
Easy Python script to get oll.tv channel links for any stream player like VLC

Скрипт котрий робить перегляд каналів з oll.tv дещо зручнішим.

## Запуск
Скрипту не потрібно передавати параметри, всі налаштування вводяться в файлі
```bash
python olltv.py
```

## Налаштування скрипта
Адреса на котрій буде доступний веб інтерфейс:
```python
HOST_NAME = '127.0.0.1'  # localhost
```
Порт:
```python
PORT_NUMBER = 8085  # port parameter
```

Деякі параметри вашого телефону чи планшету, що *вже зареєестрований в системі*! Без них ви не побачите список каналів зі своєї підписки:
```python
parameters = {
```
WLAN MAC адреса вашого телефону:
```python
    'mac': 'AB-12-34-BC-56-78',
    # mac example: 'AB-12-34-BC-56-78'
```
Назва вашого телефону / планшету:
```python
    'device': 'm2 note',
    # device example: 'm2 note'
```
Серійний номер (наразі не знаю як його дістати окрім як переглянути виходящий трафік телефону, можливо то додаток oll.tv стровює цей серійний номер):
```python
    'serial': '12ab34c5-678d-9012-ef34-abcd1234ef56:m2 note.m2note:10'
    # serial example: '12ab34c5-678d-9012-ef34-abcd1234ef56:m2 note.m2note:10'
}
```

Режим налагодження. Якщо все працює, то можете виключити змінивши 1 на 0.

```python
debug = 1  # console debug mode 1 - on / 0 - off
```

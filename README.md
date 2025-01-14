# WindGame

WindGame — это текстовая музыкальная игра, которая проверяет вашу скорость набора текста и синхронизацию с музыкальным сопровождением. Выберите уровень, наслаждайтесь музыкой, набирайте текст из песен и старайтесь не ошибаться!

## 📋 Основные возможности
- **Музыкальные уровни**: синхронизация с `.mp3` и `.lrc` файлами.
- **Режимы скорости**: обычный, nightcore (ускорение) и daycore (замедление).
- **Оценка сложности уровней**: автоматическая система подсчёта на основе длительности и сложности текста.
- **Текстовая графика**: интерфейс игры построен на библиотеке `curses`.

## 🛠️ Установка и запуск

### Требования
- Python 3.8+
- Установленные зависимости из `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### Установка
1. Склонируйте репозиторий:
   ```bash
   git clone git@github.com:automatick/WindGame.git
   cd WindGame
   ```
2. Убедитесь, что у вас установлены зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите игру:
   ```bash
   python3 main.py
   ```

## 🎮 Как играть
1. Выберите уровень из меню.
2. Выберите режим скорости:
   - **Normal** — обычная скорость.
   - **Nightcore** — ускоренное воспроизведение.
   - **Daycore** — замедленное воспроизведение.
3. Музыка начнётся, и строки текста будут появляться на экране.
4. Ваша задача — вводить текст как можно точнее и быстрее.
5. По окончании уровня будет подсчитано количество ошибок.

## 📂 Структура проекта
```plaintext
WindGame/
├── levels/            # Папка с уровнями (.mp3 и .lrc файлы)
├── main.py            # Точка входа в игру
├── engine.py          # Логика игры: обработка текста и аудио
├── mainmenu.py        # Меню выбора уровней
├── config.py          # Конфигурация игры
├── README.md          # Документация проекта
└── requirements.txt   # Зависимости Python
```

### Формат уровней
- **.mp3**: аудиофайл уровня.
- **.lrc**: файл с текстом, синхронизированным с музыкой.
  Пример `.lrc` файла:
  ```plaintext
  [00:12.00]This is the first line of lyrics
  [00:15.00]Here comes the second line
  ```

## 💡 Советы по игре
- Выбирайте режим **Daycore**, если хотите попрактиковаться.
- Тренируйте скорость и точность на сложных уровнях.
- Добавляйте свои любимые песни в папку `levels`.

## 🧩 TODO
- Добавить поддержку нескольких языков.
- Улучшить алгоритм оценки сложности уровней.
- Добавить таблицу лидеров для соревнования с друзьями.

## 🛠️ Разработчики
- **Automatick** — основная разработка, идеи и реализация.

## 📝 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

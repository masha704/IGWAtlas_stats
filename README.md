# IGWAtlas statistic

Приложение с графическим интерфейсом для анализа и визуализации статистики по
[базе данных внутренних волн в Мировом океане](https://lmnad.nntu.ru/en/igwatlas/)

Инструкция по созданию `.EXE` файла на windows:

1. Через командную строку Windows устанавливаем pyinstaller:
    ```
    pip install pyinstaller
    ```
2. В командной строке переходим в папку, где находится файл:
   ```
   cd c:\IGWAtlas_stats 
   ```
3. В командной строке набираем команду
   ```
   pyinstaller --windowed --hidden-import=pkg_resources.py2_warn --onefile --name="IGWAtlas_Stats" --icon="images/app.ico" --version-file version.txt main.py 
   ```

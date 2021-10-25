# Руководство к проекту

Ход работы подробно описан в файле sentiment.ipynb.

Файлы с расширением .tsv содержат данные, использованные в ходе проекта.

Код веб-скрэйпера, использованного для сбора обучающей выборки, находится в папке ym_scraping.

## Как запустить код
Ход работы, включая результаты вычислений, можно увидеть в файле sentiment.ipynb прямо на гитхабе. Но при желании код можно запустить локально. 
Для этого потребуется python версии 3.8.10 с установленными pip и jupyter notebook.

### На Linux:

1. Загрузите репозиторий.
```
mkdir /путь/к/проекту
cd /путь/к/проекту

git init
git pull https://github.com/eynhcaysem/sentiment-analysis-coursera main
```

2. Создайте виртуальное окружение с помощью модуля venv, активируйте его, а затем загрузите все зависимости, указанные в файле requirements.txt.
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

3. Загрузите модель для лемматизации.
```
python3 -m spacy download ru_core_news_sm
```

4. Чтобы использовать виртуальное окружение в jupyter notebook, добавьте его с помощью ipykernel.
```
python3 -m ipykernel install --user --name=env
```

5. Наконец, запустите jupyter notebook, где виртуальную среду можно будет выбрать в правом верхнем углу, открыв файл sentiment.ipynb.
```
jupyter notebook
```

### На Windows:
Единственное отличие - для активации виртуального окружения следует написать `env\Scripts\activate`.

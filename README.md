# Dialog Classifcation and Replicas Topic Modeling

Задачи:
1. <span style="color:green">&#x2713;</span> Провести классификацию диалогов, состоящих из реплик только менеджера по категориям:
   * Бизнес-карта
   * Зарплатные проекты
   * Открытие банковского счета
   * Эквайринг
2. <span style="color:darkorange">&#x26A0;</span> Провести тематическое моделирование реплик менеджера, приблизив его к заданным темам

Подробнее в `tasks.txt`

### Репозиторий содержит
- Первичный анализ датасета в `00-EDA.ipynb`
- Ход решения задачи классфикации и метрики в `01-dialog_classification.ipynb`
- Наработки решения задачи тематического моделирования в `02-topic_modeling.ipynb`
- Код для классификации отдельно взятой таблицы в `classify.py`

Идеи и ход мысли подробнее описаны в ноутбуках, приятного чтения!

### Инструкция по установке
1. `git clone https://github.com/DmitryKuznetsov1/dialog_classification_and_topic_modeling`
2. `cd dialog_classification_and_topic_modeling`
3. Положить файл `topic_modeling_task_sample_trainPart.csv` в папку `data`
4. `python3 -m venv venv`
5. `./venv/bin/pip install -r requirements.txt`

### Классифицировать отдельный файл
Чтобы классифицровать диалоги внутри произвольной таблицы dialogs.csv, нужно выполнить команду:
```./venv/bin/python3 classify.py --path/to/csv_file```

В таблице должно быть поле с диалогами `text_employer`, файл модели тяжелый, он появится после выполнения ноутбука 
`01-dialog_classification.ipynb`. Либо можно связаться со мной, пришлю ссылку на гугл-диск.

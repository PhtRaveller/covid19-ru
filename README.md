# [Дашборд распространения CoVID-19 в России](http://covid19.datarythmics.com/)

Содержит визуализации данных об эпидемии CoVID-19 в России из различных источников.

# Данные

Директория `data` содержит дампы в формате CSV из различных источников:

- `covid_stats.csv`: дневная статистика случаев по регионам и стране в целом, включая выздоровевших и умерших. Источник данных: [стопкоронавирус.рф](https://xn--80aesfpebagmfblc0a.xn--p1ai/). Отчеты Коммуникационного центра Правительства России обычно публикуются утром и соответствующие файлы обновляются как можно быстрее,
- `swabs_rpn.csv`: данные о тестировании от [Роспотребнадзора](https://www.rospotrebnadzor.ru/). Данные за 30 марта 2020 - 1 апреля 2020 выглядят противоречиво, а некоторые данные отсутствуют (например, за 29 марта 2020). Данные публикуются в течение дня (точное время неизвестно: на сайте Роспотребнадзора указаны только даты),
- `swabs_rpn_clean.csv`: очищенная версия данных о тестировании. В частности, исключены противоречивые данные, а дневное количество тестов для соответствующего периода получено интерполяцией. Начиная со 2 апреля данные выглядят полными и непротиворечивыми,
- `moscow`: данные по Москве, включая
  - `transport.csv`: дневную статистику общественного и личного транспорта, публикуемую [Дептрансом Москвы](https://t.me/DtRoad) (снижение относительно соответствующего периода 2019 года). Данные публикуются утром,
  - `hospitals`: данные, публикуемые главврачами нескольких московских больниц, работающих с CoVID-19, включая количество случаев, количество пациентов в ОРИТ (отделения реанимации и интенсивной терапии) и др. В нескольких случаях данные содержат пробелы, а поля не согласованы между больницами. Несмотря на это, данные представляют огромную ценность для оценки текущей ситуации. В большинстве случаев главврачи публикуют данные утром.

Даты во всех случаях означают дату публикации. Поэтому, например, данные Правительства России и данные Роспотребнадзора по тестированию фактически расходятся на один день. На графике тестирования эта разница скорректирована.

---
# [Dashboard for CoVID-19 in Russia](http://covid19.datarythmics.com/)

This dashboard contains visualizations of various data sources on CoVID-19 epidemic in Russia.

# Data

`data` directory contains constantly updated CSV dumps from various sources:

- `covid_stats.csv`: daily cases per region, including recovered and died, extracted from [стопкоронавирус.рф](https://xn--80aesfpebagmfblc0a.xn--p1ai/). Government reports are usually released **in the morning** and this file is updated as soon as possible,
- `swabs_rpn.csv`: swabs data from [Rospotrebnadzor](https://www.rospotrebnadzor.ru/), Russian counterpart of CDC. Apparently, data is inconsistent for 30 Mar 2020  - 1 Apr 2020. Some values are missing from reports (e. g. 29 Mar 2020). This data is released during the day (exact timing is not known) and is updated on a best effort basis,
- `swabs_rpn_clean.csv`: cleaned version of `swabs_rpn.csv` with inconsistent values removed. Daily swabs counts were interpolated for inconsistent periods. Apparently, data looks consistent and full starting from 2 Apr,
- `moscow`: Moscow data, including
  - `transport.csv`: daily public and private transport stats reported by [Moscow transportation authority](https://t.me/DtRoad) (all numbers are relative to the corresponding date of 2019). Data is released in the morning and dump is updated as soon as possible,
  - `hospitals`: data, provided by chief medical officers of some of the Moscow CoVID-19 hospitals, including cases, ICU admissions. etc. This data contains some gaps, and fields are not always consistent between hospitals, but overall this is an invaluable piece of data. Most of CMOs release the data in the morning and corresponding files are updated as soon as possible.

All dates mean dates of release. Hence, Russian government data and Rospotrebnadzor swabs data actually shifted by one day from one another. This was corrected on swabs plot. 

# Deployment

## Initial setup

First, create virtual environment:

```bash
python3 -m venv covid19
source covid19/bin/activate
```

Next, install all the dependencies:

```bash
pip3 install -r requirements.txt
```

## Serving

To run Flask dev server:

```bash
flask run --reload
```

There are many options to deploy the app, and Heroku is used at the moment (see `Procfile`). There are no specifics, which prevent this app from beaing served by any common mechanism for Flask application.

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
- `krasnodar`: данные по Краснодарскому краю, включая
  - `cases.csv`: дневные сводки с [сайта](https://admkrai.krasnodar.ru/content/1971/) Администрации Краснодарского края. Пример разбора [новости](https://admkrai.krasnodar.ru/content/1971/show/534514/):
    > В Краснодарском крае выздоровели 1139 {**`discharges`**} человек с диагнозом коронавирус
    >
    > Дата: 16 Мая 2020, Суббота 11:03
    >
    > Событие: Стационарное лечение продолжают 1316 пациентов. За последние сутки выявлено 92 {**`daily cases`**} новых случая заражения инфекцией.
    >
    > В Краснодаре заболели 35 человек, в том числе годовалый ребенок и 14-летний подросток. 8 случаев выявлено в Каневском районе, среди зараженных 8-летний ребенок. 7 случаев – в Кавказском районе. В Апшеронском районе заболели 6 человек, в том числе дети 6 и 10 лет. В Усть-Лабинском и Тихорецком районах – по 5 человек, в Тихорецком диагноз подтвержден у 2-х летнего ребенка и 17-летнего подростка.
    >
    > По 4 заболевших в Гулькевичском и Мостовском районах, в Мостовском это, в том числе 9-летний ребенок. В Армавире выявлено три новых случая коронавируса, в Староминском и Отрадненском районах – по два. По одному – в Тблисском, Щербиновском, Ейском, Северском, Славянском, Приморско-Ахтарском, Лабинском районах, а также в Сочи, Геленджике, Новороссийске и Горячем Ключе. {**`counties.csv`**}
    >
    > Возраст заболевших от 1 до 91 года. Среди них 57 {**`females`**} женщин и 35 {**`males`**} мужчин.
    >
    > Всего на 16 мая в медицинские организации края с подозрением на COVID-19 обратилось 6462 {**`covid suspected`**} человека, в том числе 698 {**`covid suspected - children`**} детей. Продолжают стационарное лечение с подозрением на коронавирус 2377 {**`hospitalized`**} человек, их них 177 {**`hospitalized - children`**} детей. Под медицинским наблюдением в поликлиниках по месту жительства находится 12633 {**`at home`**} человека.
    >
    > Лабораториями Роспотребнадзора проведено 36240 {**`tests`**} исследований, лабораториями минздрава – 94967 {**`MZ tests`**}.
    >
    > Всего на Кубани 2510 {**`confirmed tests`**} подтвержденных случаев заболевания коронавирусом. Среди зараженных 141 ребенок. 1139 {**`discharges`**} пациентов выписаны с выздоровлением, в том числе 160 человек за последние сутки. 32 {**`ventilation`**} пациента находится в тяжелом состоянии на ИВЛ. 24 {**`deaths`**} человека умерли.
    >
    > В обсерваторах размещено 2060 {**`observation`**} человек: 778 – в Краснодаре, 652 – в Сочи, 24 – в Темрюкском районе, 64 – в Кущевской, 52 – в Геленджике, 181 – в Туапсе, 19 – в Армавире, 211 – в Анапе, 79 – в Ейске. Температура у всех в норме, состояние удовлетворительное. За все время в обсерваторах выявлено 35 {**`observation - CoVID`**} положительных результатов тестов на коронавирус.
  - `counties.csv`: дневные данные по районам края.

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

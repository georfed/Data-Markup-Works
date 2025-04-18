## Инструкция по разметке классов фотошоп-запросов

Привет!

Положи, пожалуйста, файлики `markup_gradio.py` и `to_markup.csv` в одну папку,\
затем запусти скрипт:
```commandline
chmod -x ./markup_gradio.sh
python markup_gradio.sh
```
Это gradio-интерфейс, он развернётся на localhost и напишет, по какому порту.\
Перейдя по ссылке, ты попоадёшь в следующий интерфейс:

Сверху будет блок `Инструкция`, в нём будет  текст фотошоп-запроса на английском.

Затем будут кнопки, сгруппированные в 7 категорий вот так:

## addition
    'add' - добавление чего-либо
    'add clothes' - добавление именно одежды
    'add text' - добавление текста

## removal
    'remove' - удаление чего-либо
    'remove bg' - удаление фона
    'remove text' - удаление текста
    'remove watermarks - удаление ватермарок

## replacing
    'replace' - заменить что-то на что-то
    'replace text' - заменить один текст на другой

## changing
    'change' - изменить что-то
    'change color' - перекрасить что-то
    'change size' - сделать что-то больше/меньше
    'change clothes' - поменять одежду
    'change expression' - сменить выражение лица
    'change hair' - изменить волосы/причёску
    'change bg' - сменить фон
    'change weather' - смена погоды
    'change season' - смена сезона
    'change time' - смена времени суток
    'move' - передвинуть что-то
    'face swap' - поменять лица местами

## enhancing
    'enhance colors' - усилить/сбалансировать цвета
    'enhance image' - общее улучшение изображения
    'deblur' - убрать размытие
    'blur' - добавить размытие 
    'restore photo' - реставрация старых фото
    'colorize' - колоризация монохромных фото
    'better' - запрос типа "сделай лучше"
    'upscale' - увеличение разрешения
    'outline' - обводка чего-то
    'stylize' - стилизация (нарисуй в таком-то стиле)
    'filter' - наложи какой-нибудь фильтр

## common
    'memorial' - улучшение портрета и придание ему эстетичного, памятного вида 
    'profile' - улучшение портрета и придание ему формального вида, как на документы

## person
    'makeup' - нанесение/улучшение/изменение макияжа
    'age' - смена возраста (старение/омоложение)
    'muscular' - накачать мышцы
    'thinner' - сбросить лишний вес человеку, сделать стройнее


Нужно нажать на все кнопки, которые отражают запрашиваемые в тексте изменения.

Это может быть только одна кнопка, может быть несколько...

> Есть ряд ситуаций, когда не стоит выбирать ни одну категорию, а просто нажать "Далее":
> - это не запрос, а что-то непонятное\
>  *(Download Adobe InDesign CC 2017 Full Crack - Hướng dẫn chi tiết cài đặt)*
> - запрос не на редактирование одного фото (несколько фото, создание с нуля, и т.д.)
>  
> - запрос слишком абстрактный, не понятно, что нужно делать\
> *([Specific] Black and Gold Gunner Custom)*
> - запрос слишком сложный (очень много операций, работа с несколькими фото, супер-сложные подробности)\
> *(I am having an all girls youth wrestling tournament in Dec. I am trying to create singlets for the first 50 to sign up. I would like to have the text removed, the border turned to yellow and the girl wrestlers left and everything besides the border and girl wrestlers to be transparent. Thank you!)*
> - запрос абсурдный\
> *([Random] Please photoshop my mates neck so it becomes a bendy snake with his face/head still on the end. If you could get "U Wot m8" coming out his mouth that would be even better.)*

Как только появится завершающий экран, в папку со скриптом сохранится файл `done_markup.csv`.\
Отправь его мне пожалуйста!

### Спасибо за работу!)
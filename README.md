Приложение с web-интерфейсом для учета школьного спортивного инвентаря.
Приложение предоставляет различные уровни доступа для пользователей и администраторов, позволяет вести учет инвентаря, распределять его среди пользователей, а также планировать закупки и формировать отчёты.

![image](https://github.com/user-attachments/assets/9a7d2a26-d96f-4f2e-90a1-c335723495e1)


Ссылка на видео: 

Логин и пароль нейтрального пользователя без прав администратора:
Логин: user   Пароль: user123456
Логин: user2   Пароль: user123456

Логин и пароль нейтрального пользователя с правами администратора:
Логин: admin   Пароль: admin123456


Для корректной работы проекта на устройстве, где происходит запуск, должен быть установлен Python, фреймворк Django и модуль virtualenv. Python можно установить на официальном сайте (https://www.python.org/downloads/). Django нужно будет установить через командную строку командой: pip install django. Virtualenv нужно будет установить через командную строку командой: pip install virtualenv. Присутствие интернет соединения обязательно.

Чтобы скачать проект нужно установить ZIP-файл по инструкции на изображении ниже.
![image](https://github.com/user-attachments/assets/ff140126-2943-484c-814d-abb4538eaf06)

После скачивания проекта и необходимых компонентов, нужно перейти в папку с проектом, находящуюся в "Загрузках" на вашем устройстве и в терминале (вызывающимся путём нажатия сочетания клавиш Win + R и вписыванием CMD в открывшемся окне) с помощью команды консоли «cd C:\ваш\путь\до\папки\predprof-case-5-main» перейти в папку «predprof-case-5-main» скачанного проекта. После надо написать в тот же терминал команду virtualenv venv, которая создаст виртуарную среду в указанной папке (если на данном этапе по какой-то причине появляется ошибка можно попробовать альтернативу: python3 -m venv venv), дальше нужно активировать виртуальную среду командой venv\Scripts\activate 
После этих действий перед путём к указанной папке в терминале должна появиться приписка (venv).
![image](https://github.com/user-attachments/assets/a3fab775-91b8-4599-9107-c81d19418333)

Далее в командной строке нажно ввести команду pip install django, а затем python manage.py runserver, либо py -3 manage.py runserver если устройство это ноутбук. После этого консоль выведет подобное сообщение:
![image](https://github.com/user-attachments/assets/d2d56dd5-e4fe-492a-b90f-7eae92af1191)

Далее следует нажать на появившуюся ссылку и вы попадёте на сайт.

*локальный сервер для сайта запускается на вашем устройстве, чтобы после завершения работы с сайтом его отключить нажмите сочетание Ctrl + C в терминале
**для отключения виртуальной среды введите команду deactivate в терминале

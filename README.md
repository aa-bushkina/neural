# Обучение автономного управления автомобилями с использованием NEAT
## Описание проекта
Данный проект представляет собой реализацию алгоритма NeuroEvolution of Augmenting Topologies (NEAT) для обучения нейронных сетей управлять автомобилями на дороге. В проекте используется библиотека Pygame для создания визуализации и взаимодействия с окном отображения.

## Структура проекта
- config_variables.py: Файл содержит переменные конфигурации, такие как параметры автомобилей, дороги и нейронных сетей. 
- config_file.py: Файл содержит переменные конфигурации нейронной сети
- car.py: В этом файле содержится код для класса Car, представляющего автомобиль и его функции. 
- world.py: Файл world.py содержит класс World, который описывает игровой мир и его функции. 
- NNdraw.py: В данном файле находятся класс NN, отвечающий за визуализацию узлов нейронных сетей. 
- connection.py: В данном файле находятся класс Connection, отвечающий за визуализацию узлов нейронных сетей. 
- node.py: Файл содержит класс Node, который используется для представления узлов нейронных сетей. 
- road.py: В этом файле содержится класс Road, описывающий дорогу и ее параметры. 
- coordinates.py: Класс для работы с точками.
- main.py: Основной исполняемый файл проекта, который запускает NEAT алгоритм для обучения нейронных сетей и визуализирует процесс.
## Зависимости
Для запуска проекта необходимо установить следующие зависимости:
- Python 3.x 
- Pygame 
- NEAT (NeuroEvolution of Augmenting Topologies)
## Запуск проекта
Установите все необходимые зависимости, выполнив pip install pygame, pip install neat-python
Запустите файл main.py, чтобы начать обучение нейронных сетей.
После запуска вы увидите визуализацию дороги и автомобилей, а также прогресс обучения на экране.
## Дополнительные сведения
Конфигурация NEAT алгоритма задается в файле config_file.txt.
Изменения параметров автомобилей, дороги и нейронных сетей можно вносить в соответствующие переменные в файле config_variables.py.
## Описание
Приложение представляет собой симуляцию, где автомобили учатся двигаться по дороге, используя нейронные сети для принятия решений. 
Вначале генерируется случайная дорога с изгибами и другими характеристиками. Затем создается начальная популяция автомобилей, каждый из которых оснащен нейронной сетью. Эти сети обучаются в процессе симуляции движения по дороге.
Каждый автомобиль получает информацию о своем окружении с помощью датчиков, после чего нейронная сеть анализирует эту информацию и принимает решения о том, как реагировать на окружающую обстановку. На основе этих решений автомобиль двигается по дороге.
В процессе движения автомобили накапливают опыт, и их нейронные сети постепенно улучшают свои навыки управления. Это происходит благодаря алгоритму обучения, который корректирует параметры сетей на основе их производительности в симуляции.
В конечном итоге, после множества итераций обучения, автомобили становятся все более эффективными в управлении, что позволяет им успешно преодолевать сложные участки дороги.
## Авторы
1. Бушкина А.О.
2. Свайкин И.С.
3. Столбов С.В.

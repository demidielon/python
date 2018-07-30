def clear():
    """
    Функция для очистки консоли перед выводом/вводом данных
    """
    print("\n" * 100)


def interface(tasks):
    """
    Интерфейс
    Задания для интерфейса передаются в виде словаря
    tasks = {'команда интерфеса': (задача/фуккция, описания задачи, аргументы),... }
    """

    clear()

    alert = ''
    # Выводим список заданий
    for key, task in tasks.items():
        alert += '[{}] {}\n'.format(key, task[1])

    alert += '[q] Завершить работу\n\nВыберите действие: '

    # Получаем ответ пользователя
    answer = ''
    result = ''
    while answer not in ('q', 'Q'):
        answer = input(alert)
        if answer in tasks:
            try:
                result = tasks[answer][0](tasks[answer][2])
            except:
                try:
                    result = tasks[answer][0](tasks[answer][2][0], tasks[answer][2][1])
                except:
                    result = tasks[answer][0]()
        elif answer in ('q', 'Q'):
            pass
        else:
            print('Указанная задача не найдена\n')

    print('Спасибо, за использования нашего программного обеспечения, удачи.')
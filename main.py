
import json


def json_loader():

    try:
        with open('todo.json','r',encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('файл не найден')
        data = []
    except json.JSONDecodeError:
        print('файл повреждён')
        data = []

    return data


global_task = json_loader()

def menu():
    print('выберите действие')
    print('1. Показать все задачи')
    print('2. Добавить задачу')
    print('3. Отметить задачу как выполнено')
    print('4. Удалить задачу')
    print('5. Менять текст задачи по ID: ')
    print('6. Переключение статуса задачи')
    print('7. Фильтр по статусу')
    print('8. Искать задачу')
    print('9. Сортировать по имени')
    print('10. Завершить работу')


def show_tasks(tasks):
    print_tasks(tasks)


def get_task_id():
    task_id_str = input('Введите ID задачи: ')
    if not task_id_str:
        print('ID не может быть пустым')
        return None
    try:
        task_id = int(task_id_str)
        return task_id
    except ValueError:
        print('ID должен быть числом')
        return None

def add_task(tasks):

    next_id = max([i.get('id',0) for i in tasks],default=0)+1
    new_title = input('Введите название задачи: ')
    if not new_title:
        print('название не может быть пустым')
        return

    new_task = {
        'id':next_id,
        'title':new_title,
        'done':False
    }

    tasks.append(new_task)
    save_data(tasks)
    print('Задача добавлена')


def save_data(tasks):
    with open('todo.json','w',encoding='utf-8') as file:
        json.dump(tasks,file,ensure_ascii=False,indent=4)


def done_task(tasks):
    task_id = get_task_id()
    if task_id is None:
        return

    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            save_data(tasks)
            print('Задача отмечена как выполненная')
            return
    print('нет такого id')


def delete_task(tasks):
    task_id = get_task_id()
    if task_id is None:
        return

    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_data(tasks)
            print('Задача удалена')
            return
    print('нет такого id')


def change_title(tasks):
    task_id = get_task_id()
    if task_id is None:
        return

    for task in tasks:
        if task['id'] == task_id:
            new_title = input('Введите новое название задачи: ')
            task['title'] = new_title
            save_data(tasks)
            print('Название задачи изменено')
            return
    print('нет такого id')

def toggle_task(tasks):
    task_id = get_task_id()
    if task_id is None:
        return

    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            save_data(tasks)
            print("Статус задачи переключён")
            return
    print('нет такого id')


def filter_tasks(tasks):
    print('выберите задачи которые хотите увидеть')
    print('1. выполненные задачи')
    print('2. не выполненные задачи')
    oper = input('введите действие: ')
    if oper == '1':
        filtered = [t for t in tasks if t['done']]
    elif oper == '2':
        filtered = [t for t in tasks if not t['done']]
    else:
        print('Неизвестное действие')
        return
    print_tasks(filtered)

def search_tasks(tasks):
    name = input('введите название: ').lower()
    filtered = [t for t in tasks if name in t['title'].lower()]
    if not filtered:
        print("Задачи с таким названием не найдены.")
    else:
        print_tasks(filtered)


def sort_tasks(tasks):
    tasks.sort(key=lambda x:x['title'])
    print("Задачи отсортированы по названию:")
    print_tasks(tasks)


def print_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return

    print("\nСписок задач:")
    print("-" * 50)
    print(f"{'ID':<5} {'Название задачи':<35} {'Статус'}")
    print("-" * 50)

    for task in tasks:
        status = '✅' if task['done'] else '❌'
        print(f"{task['id']:<5} {task['title']:<35} {status}")

    print("-" * 50)


while True:
    print()
    menu()
    op = input('введите действие: ')

    if op == '1':
        show_tasks(global_task)
    elif op == '2':
        add_task(global_task)
    elif op == '3':
        done_task(global_task)
    elif op == '4':
        delete_task(global_task)
    elif op == '5':
        change_title(global_task)
    elif op == '6':
        toggle_task(global_task)
    elif op == '7':
        filter_tasks(global_task)
    elif op == '8':
        search_tasks(global_task)
    elif op == '9':
        sort_tasks(global_task)
    elif op == '10':
        break
    else:
        print('неизвестное действие')


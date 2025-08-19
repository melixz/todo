import requests
from getgauge.python import step, before_scenario, after_scenario

BASE_URL = "http://localhost:8000"
created_tasks = []


@before_scenario
def setup():
    global created_tasks
    created_tasks = []


@after_scenario
def cleanup():
    global created_tasks
    for task_id in created_tasks:
        try:
            requests.delete(f"{BASE_URL}/tasks/{task_id}")
        except requests.RequestException:
            pass
    created_tasks = []


@step("Создать задачу с названием <title> и описанием <description>")
def create_task(title, description):
    global created_tasks

    payload = {"title": title, "description": description, "status": "создано"}

    response = requests.post(f"{BASE_URL}/tasks/", json=payload)
    assert response.status_code == 201, f"Ошибка создания задачи: {response.text}"

    task_data = response.json()
    created_tasks.append(task_data["id"])

    globals()["last_created_task"] = task_data


@step("Проверить что задача создана со статусом <expected_status>")
def verify_task_status(expected_status):
    task = globals().get("last_created_task")
    assert task is not None, "Задача не была создана"
    assert task["status"] == expected_status, (
        f"Ожидался статус '{expected_status}', получен '{task['status']}'"
    )


@step("Получить список всех задач")
def get_all_tasks():
    response = requests.get(f"{BASE_URL}/tasks/")
    assert response.status_code == 200, (
        f"Ошибка получения списка задач: {response.text}"
    )

    tasks = response.json()
    globals()["all_tasks"] = tasks


@step("Проверить что в списке есть <count> задачи")
def verify_tasks_count(count):
    tasks = globals().get("all_tasks", [])
    expected_count = int(count)
    actual_count = len(tasks)
    assert actual_count >= expected_count, (
        f"Ожидалось минимум {expected_count} задач, получено {actual_count}"
    )


@step("Проверить что в списке есть 2 задачи")
def verify_two_tasks():
    verify_tasks_count("2")


@step("Обновить статус задачи на <new_status>")
def update_task_status(new_status):
    task = globals().get("last_created_task")
    assert task is not None, "Задача не была создана"

    task_id = task["id"]
    payload = {"status": new_status}

    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200, f"Ошибка обновления задачи: {response.text}"

    globals()["last_created_task"] = response.json()


@step("Проверить что статус задачи изменился на <expected_status>")
def verify_updated_status(expected_status):
    task = globals().get("last_created_task")
    assert task is not None, "Задача не найдена"
    assert task["status"] == expected_status, (
        f"Ожидался статус '{expected_status}', получен '{task['status']}'"
    )


@step("Удалить созданную задачу")
def delete_task():
    task = globals().get("last_created_task")
    assert task is not None, "Задача не была создана"

    task_id = task["id"]
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 204, f"Ошибка удаления задачи: {response.text}"

    if task_id in created_tasks:
        created_tasks.remove(task_id)


@step("Проверить что задача удалена")
def verify_task_deleted():
    task = globals().get("last_created_task")
    assert task is not None, "Задача не была создана"

    task_id = task["id"]
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 404, (
        f"Задача не была удалена, статус: {response.status_code}"
    )

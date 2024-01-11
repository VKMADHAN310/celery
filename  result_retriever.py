from celery.result import AsyncResult
import time


def get_task_result(task_id):
    result = AsyncResult(task_id)

    # Wait for the task to complete (adjust the timeout as needed)
    result_value = result.get(timeout=10)

    return result_value


if __name__ == "__main__":
    task_id = input("Enter task ID: ")
    result = get_task_result(task_id)
    print(result)

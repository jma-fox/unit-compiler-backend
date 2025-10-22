import pandas as pd


def get_task_data(task_file):
    task_data = pd.read_csv(task_file)

    return task_data
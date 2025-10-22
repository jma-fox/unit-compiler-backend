import pandas as pd


def get_unit_data(unit_file):
    unit_data = pd.read_csv(unit_file)

    return unit_data

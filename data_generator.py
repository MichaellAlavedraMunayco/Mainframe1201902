import numpy as np
import pandas as pd


def random_date(start_date, range_in_days, size):
    days_to_add = np.arange(0, range_in_days)
    return np.sort([np.datetime64(start_date) + np.random.choice(days_to_add) for i in range(size)])


def generate_date_profit():

    ds = dict(
        size=1500,
        col=dict(
            mean=dict(
                profit=1000000
            ),
            sdev=dict(
                profit=50000
            )
        )
    )

    date = np.array(random_date("2015-01-01", 365 * 5, ds["size"]), dtype=str)

    profit = np.absolute(np.round(np.random.normal(
        ds["col"]["mean"]["profit"], ds["col"]["sdev"]["profit"], ds["size"]), 3))

    dataset = np.column_stack((date, profit))

    df = pd.DataFrame(dataset, columns=['Date', 'Profit'])

    df.to_csv('static/date_profit.csv', index=None, header=True)


def generate_demand_profit():

    ds = dict(
        size=1500,
        col=dict(
            mean=dict(
                demand=650000,
                profit=1000000
            ),
            sdev=dict(
                demand=60000,
                profit=50000
            )
        )
    )

    demand = np.absolute(np.round(np.random.normal(
        ds["col"]["mean"]["demand"], ds["col"]["sdev"]["demand"], ds["size"]), 0))

    profit = np.absolute(np.round(np.random.normal(
        ds["col"]["mean"]["profit"], ds["col"]["sdev"]["profit"], ds["size"]), 3))

    dataset = np.column_stack((demand, profit))

    df = pd.DataFrame(dataset, columns=['Demand', 'Profit'])

    df.to_csv('static/demand_profit.csv', index=None, header=True)


generate_demand_profit()

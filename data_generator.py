import numpy as np
import pandas as pd
from descriptive_stadistics import get_media_aritmetica
from descriptive_stadistics import get_desviacion_tipica

amount_range = [300000, 500000, 1000000, 1500000]

ds = dict(
    size=700000,
    col=dict(
        mean=dict(
            profit=get_media_aritmetica(amount_range)
        ),
        sdev=dict(
            profit=get_desviacion_tipica(amount_range)
        )
    )
)


def random_date(start_date, range_in_days, size):
    days_to_add = np.arange(0, range_in_days)
    return np.sort([np.datetime64(start_date) + np.random.choice(days_to_add) for i in range(size)])


date = np.array(random_date("2015-01-01", 365 * 5, ds["size"]), dtype=str)

profit = np.absolute(np.round(np.random.normal(
    ds["col"]["mean"]["profit"], ds["col"]["sdev"]["profit"], ds["size"]), 3))

dataset = np.column_stack((date, profit))

df = pd.DataFrame(dataset, columns=['Date', 'Profit'])

df.to_csv('static/date_profit.csv', index=None, header=True)

print(df)

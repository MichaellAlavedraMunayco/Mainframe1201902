import numpy as np
from descriptive_stadistics import *

dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mean = get_media_aritmetica(dataset)
standard_desviation = get_desviacion_tipica(dataset)
s = np.random.normal(mean, standard_desviation, 20)

print(mean)
print(standard_desviation)
print(s)

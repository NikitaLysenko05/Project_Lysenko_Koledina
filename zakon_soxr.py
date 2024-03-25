import numpy as np
import pandas as pd

stex = np.array(pd.read_csv("stex_brom.txt", sep=" ").drop('Obr', axis=1))
atm = np.array(pd.read_csv("atm_brom.txt", sep=" ").drop('Unnamed: 0', axis=1))
zak_soxr = np.dot(stex, atm)
if np.count_nonzero(zak_soxr) == 0:
    print('Закон сохранения количества по стадиям выполнен!')
else:
    print('Закон сохранения количества по стадиям не выполнен!')
print(stex)
print(atm)
print(zak_soxr)

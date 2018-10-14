

import csv
import numpy as np
import math
import matplotlib.pyplot as plt


k = 0


# with open('cryptojuice1.txt', 'r') as csvfile:
#         cryptoworth = csv.reader(csvfile, delimiter = '\n')
#         for worth in cryptoworth:
#             price_list.append(int(worth[0]))
#     csvfile.close()

k = 0
while k < 10:
    j = 0
    price_list = [594]
    while j < 300:
        mu = 0.005
        vol = 0.03
        daily_returns=np.random.normal(mu,vol)+1
        price_list.append(round(price_list[-1]*daily_returns,2))
        j += 1
    plt.plot(price_list)
    k += 1

# plt.yscale('log')
plt.show()



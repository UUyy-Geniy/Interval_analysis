import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
np.float_ = np.float64
import intvalpy as ip

data_folder = Path('rawData')

files = sorted([data_folder / f for f in os.listdir(data_folder) if f.endswith('.bin')])

beta_0_int = ip.Interval(-0.0120557, -0.01095409)
beta_1_int = ip.Interval(0.79738604,  0.80082334)

beta_0_ext = ip.Interval(-0.0123111, -0.01019713)
beta_1_ext = ip.Interval(0.79662894,  0.80290599)

xs = np.array([float(file_path.name.split('_')[0]) for file_path in files])
xs_continuous = np.linspace(xs.min(), xs.max(), 100)
names = ["internal", "external"]
for i,  (beta_0, beta_1) in enumerate(((beta_0_int, beta_1_int), (beta_0_ext, beta_1_ext))):
    ys = beta_0 + beta_1 * xs_continuous
    ys_a = np.array([float(interval.a) for interval in ys])
    ys_b = np.array([float(interval.b) for interval in ys])

    plt.figure(figsize=(8, 6))
    plt.fill_between(xs_continuous, ys_a, ys_b, alpha=0.3)
    plt.plot(xs_continuous, ys_a, color='red', linewidth=0.5)
    plt.plot(xs_continuous, ys_b, color='red', linewidth=0.5)
    plt.plot(xs_continuous, (ys_a + ys_b) / 2, color='red', linewidth=0.5)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(names[i])
    plt.savefig(f"regression_{names[i]}.jpg")
    plt.show()


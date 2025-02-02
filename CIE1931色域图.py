import matplotlib.pyplot as plt
from colour.plotting.diagrams import plot_chromaticity_diagram
import numpy as np


plt.figure(figsize=(10, 8))


plot_chromaticity_diagram(
    cmfs='CIE 1931 2 Degree Standard Observer',
    source='CIE',
    title='CIE 1931 Chromaticity Diagram',
    wavelengths=np.arange(400, 701, 10)
)


ax = plt.gca()


points = [(0.7, 0.3), (0.2, 0.7)]
for (x_val, y_val) in points:
    ax.plot(x_val, y_val, 'ro')
    ax.text(x_val, y_val, f'({x_val},{y_val})', fontsize=9, ha='right')


for wavelength in np.arange(400, 701, 10):

    x, y = colour.colorimetry.CIE_1931_CMFs(wavelength)
    ax.annotate(f'{wavelength}n',
                (x, y),
                textcoords="offset points",
                xytext=(0,10),
                ha='center')


ax.set_xlabel('x')
ax.set_ylabel('y')


plt.show()
'''
INTERPOLATOR - A serie interpolator using Python
Copyright (C) 2012  Pierre Gradot

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

# Code test pour le moment


import matplotlib.pyplot as plt         # module
from scipy.interpolate import lagrange  # fonction

# Donnees sources
x = range(-100,100)
y = [ pow(i,2) for i in x ]

# Polynome et images interpolees
xr = x[50:55]
yr = y[50:55]

p = lagrange(xr,yr)
print p
yip = p(x)

# Affichage
plt.plot(x, y, 'b--', label='Originales')
plt.plot(x, yip, 'rs', label='Interpolees')
plt.legend()
plt.show()

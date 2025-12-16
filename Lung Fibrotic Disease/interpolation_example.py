import numpy as np
import matplotlib.pyplot as plt

"""LINER INTERPORLATION"""

# x_points = [1,3]
# y_points = [1,3]

# x1,x2 = 1,3
# y1, y2 = 1,3

# #make the Z and Y matrices
# Z = np.array([[1,x1],[1,x2]])
# Y = np.array([y1,y2])

# #compute A matrix
# A = np.linalg.solve(Z,Y)
# print ("A = ", A)

# a1, a2 = A
# x_value = 2
# y_value = a1+a2*x_value
# print("At x=2, y= ", y_value)

# x = np.linspace(0,5,100)
# y = a1+a2*x
# plt.plot(x,y)

# plt.scatter(x_points,y_points,color='blue',s = 60, label='known points')
# plt.scatter(x_value,y_value, color='red', zorder = 5, label=f'interpolated point (x={x_value}), y={y_value})')

# plt.title("Line with Interpolated Point (red)")
# plt.xlabel('x')
# plt.ylabel('y')
# plt.grid(True)
# plt.legend()
# plt.show()


"""Quadratic interporlation"""
x_points = [1,3,5]
y_points = [1,3,2]

x1,x2,x3=1,3,5
y1,y2,y3=1,3,2
Z = np.array([[1,x1,x1**2],[1,x2,x2**2],[1,x3,x3**2]])
Y = np.array([y1,y2,y3])
A = np.linalg.solve(Z,Y)
print("A = ", A)
a1,a2,a3 = A
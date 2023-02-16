"""Matrices oefenen"""
import numpy as np

matrix1 = [[0, 0, 1], [3, 0, 3], [1, 1, 0]]
# print(matrix1)

matrix2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print(matrix2)

# matrix3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# for i in range(len(matrix1)):
#     for j in range(len(matrix1[i])):
#         matrix3[i][j] = matrix1[i][j] + matrix2[i][j]

# print(matrix3)

matrix1 = np.matrix(matrix1)
matrix2 = np.matrix(matrix2)
matrix3 = matrix1 + matrix2
print(matrix3)


matrix4 = np.matrix([[1, 2], [3, 4], [5, 6]])
matrix5 = np.matrix([[4, 3], [2, 1]])
matrix6 = matrix4 * matrix5
print(matrix6)


matrix7 = np.matrix("1 2; 3 4; 5 6")
matrix8 = np.matrix("4 3; 2 1")
matrix9 = matrix7 * matrix8
print(matrix9)

matrix10 = np.matrix("1 2; 3 4")
matrix11 = np.asmatrix(matrix10)
print(matrix11)
matrix10[0, 0] = 5
print(matrix11)


# oefening klas
m1 = [[2, 5, 7, 8], [9, 1, 2, 4], [0, 3, 8, 6], [5, 9, 2, 3]]
m2 = [[9, 1, 2, 7], [0, 5, 4, 6], [3, 2, 1, 7], [4, 8, 2, 5]]
m3 = np.matrix(m1) * np.matrix(m2)
print(m3)

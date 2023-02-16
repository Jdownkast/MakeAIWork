list1 = [1, 2, 3]
list2 = list1
print(list2)
list1[0] = 4
print(list2)

str1 = "Origineel"
str2 = str1
print(str2)
str1 = "Aanpassing"
print(str2)

int1 = 1
int2 = 2
print(int2)
int1 = 3
print(int2)

print(id(list1) == id(list2))
print(id(int1) == id(int2))

list3 = list1 + list2
print(list3)
list1[0] = 1
print(list3)

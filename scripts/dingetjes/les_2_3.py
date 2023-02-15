inputString = input('Enter a string: ')

print(len(inputString))

for i in range(10):
    print(inputString)

print(inputString[0])
print(inputString[:3])
print(inputString[-3:])
print(inputString[::-1])
if len(inputString) > 7:
    print(inputString[7])
else:
    print("Kan niet")
print(inputString[1:-1])
print(inputString.upper())
print(inputString.replace("a", "e"))
print("_ "*len(inputString))
i = [1,5,2,5,2,5,2,3,5,2]
size = len(i)
for index in range(size):
	val = i[index]
	pointer = index
	while pointer > 0 and i[pointer - 1] > val:
		i[pointer] = i[pointer - 1]
		pointer -= 1
	i[pointer] = val
print (i)
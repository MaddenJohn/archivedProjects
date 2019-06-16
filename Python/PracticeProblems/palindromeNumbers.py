def test(num):
	maxNum  = num + 2
	stNum = str(num)
	sz = len(stNum)
	if (len(str(maxNum)) > len(str(num))):
		print (maxNum)
	else:
		index = 0 + sz//2
		while stNum[index] == "9":
			index+=1
		val = num + 10 ** (sz - index - 1)
		if (sz%2 == 0):
			val += 10 ** (index)
		print (val)

test(99)
test(12321)
test(12344321)
test(22)
test(999999)
test(1000001)
test(12399321)





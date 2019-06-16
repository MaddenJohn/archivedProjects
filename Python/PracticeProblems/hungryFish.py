def calcAdds (num, tgt):
	adds = 0
	while (num < tgt):
		num += num - 1
		adds += 1
	return (num, adds)


def helper(size, fishes, index, fishInj):
	# print(index, fishInj)
	if (index >= size):
		return 0
	tgt = int(fishes[index])
	if (fishInj > tgt):
		return min (size - index, 
		helper(size, fishes, index + 1, tgt + fishInj))
	adds = calcAdds(fishInj, tgt)
	# print (adds)
	return min (size - index, 
		adds[1] + helper(size, fishes, index + 1, tgt + adds[0]))

def test(fishes):
	fishesTot = fishes.split("#")
	fishInj = int(fishesTot[0])
	fishesReg = fishesTot[1].split(",")
	numFishies = len(fishesReg)
	print(helper(numFishies, fishesReg, 0, fishInj))


# test("10#9,20,25,100")
# test("3#25,20,100,400,500")
# test("3#25,20,100,101,102")
# test("50#25,20,9,100")
test("3#25,20,100,400,500,501,502,503")





def convertMorseCode(code, dic):
	result = ""
	code = code.upper()
	for letter in code:
		result += dic[letter]
	return result

# 3      .-.-              (3)
# 4      ..-...-.-.--      (25)
def findCombos(size, morseCode, index, dic, word):
	result = 0
	if (index > len(morseCode) - size):
		return 0
	if (size == 1):
		smallCode = morseCode[index:]
		if (morseCode[index:] in dic):
			# print (word + dic[smallCode])
			return 1 
		else:
			return 0
	for x in range(4):
		smallCode = morseCode[index:index + x + 1]
		if (morseCode[index:index + x + 1] in dic):
			# print (word + dic[smallCode])
			result += findCombos(size - 1, morseCode, index + 1 + x, dic, word + dic[smallCode])
	return result

def test(code):
	MORSE_CODE_DICT = { "A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".",
	"F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-",
	"L":".-..", "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-",
	"R":".-.", "S":"...", "T":"-", "U":"..-", "V":"...-", "W":".--",
	"X":"-..-", "Y":"-.--", "Z":"--.."}
	CODE_reversed = {'..-.': 'F', '-..-': 'X','.--.': 'P', '-': 'T', '...-': 'V',
	'-.-.': 'C', '.': 'E', '.---': 'J','-.-': 'K', '..': 'I','.-..': 'L', 
	'-.--': 'Y','.--': 'W', '....': 'H', '-.': 'N', '.-.': 'R','-...': 'B',
	 '--..': 'Z', '-..': 'D', '--.-': 'Q','--.': 'G', '--': 'M', '..-': 'U',
	  '.-': 'A', '...': 'S'}

	morseCode = convertMorseCode(code, MORSE_CODE_DICT)
	size = len(code)
	print(morseCode + " " + str(findCombos(size, morseCode, 0, CODE_reversed, "")))



test("eta")
test("Infy")
test("test")
test("InfyInfyIn")





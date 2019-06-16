import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/*
 * 
 * arguments for running: java AES option keyFile inputFile 
 * 
 * here keyFile is a key file, inputFile (no extension) names a file containing lines of plaintext, 
 * and option is "e" or "d" for encryption and decryption, respectively. 
 * keyFile contains a single line of 64 hex characters, which represents a 256-bit key. 
 * The inputFile should have 32 hex characters per line
 * 
 * As an example, if you run: 
 * java AES e key plaintext = The output should be in file plaintext.enc.
 * java AES d key plaintext.enc = The output would be in plaintext.enc.dec, and should match the original plaintext input file. 
 * Also, plaintext.enc must follow AES standards specified in the assignment page.
 * 
 * This java file is the only one for this project. This project takes in a file of hex text and uses the 256 bit key
 * Advanced Encryption Standard to encrypt text. This project also has the ability to decrypt a text using this same
 * 256 bit key. The way this works is through a process of subBytes, mixColumns, shiftRows, and roundKey methods in 
 * a 14 round cycle to modify data. The key also is different for each round, which allows for a complex way of 
 * encypting a file of data. 
 */
public class AES {

	// Values found from wikipedia
	final static int[][] sBox = {
			{ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76 },
			{ 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0 },
			{ 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15 },
			{ 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75 },
			{ 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84 },
			{ 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf },
			{ 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8 },
			{ 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2 },
			{ 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73 },
			{ 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb },
			{ 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79 },
			{ 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08 },
			{ 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a },
			{ 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e },
			{ 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf },
			{ 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 } };

	final static int[][] iSBox = {
			{ 0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb },
			{ 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb },
			{ 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e },
			{ 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 },
			{ 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92 },
			{ 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 },
			{ 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06 },
			{ 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b },
			{ 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73 },
			{ 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e },
			{ 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b },
			{ 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4 },
			{ 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f },
			{ 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef },
			{ 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 },
			{ 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d } };

	final static int[] rCon = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
			0x9a };

	/*
	 * This is the main method for the AES project. This method parses the command arguments, reads
	 * in the data from the files, and then calls the appropriate method to encrypt or decrypt the data.
	 * Finally, this method will output the data to a file. 
	 */
	public static void main(String[] args) throws IOException {
		String keyName = "";
		String fileName = "";
		String option = "";
		// Parse the command line arguments
		if (args.length == 3) {
			option = args[0];
			keyName = args[1];
			fileName = args[2];
			if (!(option.equals("e") || option.equals("d"))) {
				System.err.println("Error in argument 1");
				System.exit(1);
			}
			/*if (!keyName.equals("key")) {
				System.err.println("Error in argument 2");
				System.exit(1);
			}*/
		} else {
			System.err.println("Error in number of arguments");
			System.exit(1);
		}

		File mainFile = new File(fileName);
		File keyFile = new File(keyName);
		FileReader fileReader = new FileReader(mainFile);
		BufferedReader fileBR = new BufferedReader(fileReader);
		FileReader keyReader = new FileReader(keyFile);
		BufferedReader keyBR = new BufferedReader(keyReader);

		// read in from the key file
		String key = keyBR.readLine();
		String[] keyRounds = new String[15];
		fillRounds(keyRounds, key);

		String lineText = fileBR.readLine();
		StringBuilder output = new StringBuilder();
		String newFileName = fileName;
		double startTime = System.currentTimeMillis();
		double numLines = 0.0;
		String type = "";
		// Read in from the text file to encrypt or decrypt
		while (lineText != null) {
			if (checkText(lineText)) {
				numLines++;
				if (option.equals("e")) {
					type = "Encryption ";
					lineText = padInputLine(lineText);
					String encryptText = encryptKey(lineText, keyRounds);
					output.append(encryptText + "\n");
					if (numLines == 1)
						newFileName += ".enc";
				} else if (option.equals("d")) {
					type = "Decryption ";
					String decryptText = decryptKey(lineText, keyRounds);
					output.append(decryptText + "\n");
					if (numLines == 1)
						newFileName += ".dec";
				}
			}
			lineText = fileBR.readLine();
		}
		// Write out the final data to file
		double totalTime = System.currentTimeMillis() - startTime;
		double throughPut = (numLines * 16) / 1024 / (totalTime / 1000);
		System.out.println(type +
				"Throughput: " + (numLines * 16) + " Bytes in " + totalTime + " ms " + " = " + throughPut + " MB/Sec ");
		BufferedWriter writer = new BufferedWriter(new FileWriter(newFileName));
		writer.write(output.toString());
		writer.close();
		fileBR.close();
		keyBR.close();
	}

	// Check the text for any non-hexidecimal digit. If one is found in input, then this
	// line will be ignored in the encryption process. 
	private static boolean checkText(String lineText) {
		String text = lineText.toUpperCase();
		for (char c : text.toCharArray()) {
			if (!(Character.isDigit(c) || (c <= 'F' && c >= 'A'))) {
				return false;
			}
		}
		return true;
	}

	// Pad the input line if there is less than 32 hexidecimal digits or if there are more than 32.
	private static String padInputLine(String lineText) {
		StringBuilder result = new StringBuilder(lineText);
		for (int i = lineText.length(); i < 32; i++) {
			result.append("0");
		}
		return result.toString().toUpperCase().substring(0, 32);
	}

	// Main function for decrypting the data. Goes thorugh 14 rounds of roundkey, inverse mixcolumns, 
	// inverse shiftRows and inverse subbytes. This will return the original data.
	private static String decryptKey(String finalKey, String[] keyRounds) {
		String input = finalKey;
		for (int i = 14; i > 0; i--) {
			input = roundKey(input, keyRounds[i / 2], i % 2);
			if (i != 14) {
				input = invMixColumns(input);
			}
			input = invShiftRows(input);
			input = invSubBytes(input);
		}
		input = roundKey(input, keyRounds[0], 0);
		return input;
	}

	// Main method to encrypt the data. Goes thorugh 14 rounds of roundkey, mixcolumns, 
	// shiftRows and subbytes. This will return the encrypted data.
	private static String encryptKey(String inputLine, String[] keyRounds) {
		String input = roundKey(inputLine, keyRounds[0], 0);
		for (int i = 1; i <= 14; i++) {
			input = subBytes(input);
			input = shiftRows(input);
			if (i != 14) {
				input = mixColumns(input);
			}
			input = roundKey(input, keyRounds[i / 2], i % 2);
		}
		return input;
	}

	// Method to fill in all of the round keys into an array for use later in the algorithm.
	private static void fillRounds(String[] keyRounds, String keyLine) {
		keyRounds[0] = keyLine.toUpperCase();
		for (int i = 1; i < keyRounds.length / 2 + 1; i++) {
			StringBuilder round = new StringBuilder();
			String prevKey = keyRounds[(i - 1)];
			String temp = prevKey.substring(prevKey.length() - 8);
			temp = temp.substring(2) + temp.substring(0, 2);
			temp = subBytes(temp);
			String rconTemp = temp.substring(0, 2);
			int newStart = Integer.parseInt(rconTemp, 16) ^ rCon[i - 1];
			temp = decToHex(newStart) + temp.substring(2);
			String lastBlock = temp;
			int index = 0;
			// Loops through Byte and modifies appropiately. 
			for (int j = 0; j < 8; j++) {
				lastBlock = xorBytes(prevKey.substring(j * 8, j * 8 + 8), lastBlock);
				round.append(lastBlock);
				if (j == 3) {
					lastBlock = subBytes(lastBlock);
				}
				index = (index + 1) % 4;
			}
			keyRounds[i] = round.toString().toUpperCase();
		}
	}

	// Returns xor of two 4 byte hex strings
	private static String xorBytes(String prevKey, String lastBlock) {
		StringBuilder result = new StringBuilder();
		for (int i = 0; i < 4; i++) {
			int prevKeyPart = Integer.parseInt(prevKey.substring(i * 2, i * 2 + 2), 16);
			int lastBlockPart = Integer.parseInt(lastBlock.substring(i * 2, i * 2 + 2), 16);
			result.append(decToHex(prevKeyPart ^ lastBlockPart));
		}
		return result.toString();
	}

	// Method for round key. Xors the data with the key, using the second half of
	// the stored key every other time.
	private static String roundKey(String input, String key, int second) {
		if (second == 1) {
			key = key.substring(32);
		}
		StringBuilder result = new StringBuilder();
		for (int i = 0; i < 16; i++) {
			int val = Integer.valueOf(input.substring(i * 2, i * 2 + 2), 16);
			int val2 = Integer.valueOf(key.substring(i * 2, i * 2 + 2), 16);
			int newVal = val ^ val2;
			String newByte = Integer.toHexString(newVal);
			if (newByte.length() == 1)
				newByte = "0" + newByte;
			result.append(newByte);
		}
		return result.toString().toUpperCase();
	}

	// mix columns method for reallanging the byte array. Uses method from Bill Young directly
	private static String mixColumns(String input) {
		byte[][] st = toByteArray(input);
		for (int i = 0; i < 4; i++) {
			mixColumn2(i, st);
		}
		StringBuilder result = new StringBuilder();
		transpose(st);
		for (byte[] b : st) {
			for (byte b2 : b) {
				String bitString = "" + Byte.toUnsignedInt(b2);
				String newByte = Integer.toHexString(Integer.valueOf(bitString));
				if (newByte.length() == 1)
					newByte = "0" + newByte;
				result.append(newByte);
			}
		}
		return result.toString().toUpperCase();
	}

	// mix columns method for reallanging the byte array. Uses method from Bill Young directly
	private static String invMixColumns(String input) {
		byte[][] st = toByteArray(input);
		for (int i = 0; i < 4; i++) {
			invMixColumn2(i, st);
		}
		StringBuilder result = new StringBuilder();
		transpose(st);
		for (byte[] b : st) {
			for (byte b2 : b) {
				String bitString = "" + Byte.toUnsignedInt(b2);
				String newByte = Integer.toHexString(Integer.valueOf(bitString));
				if (newByte.length() == 1)
					newByte = "0" + newByte;
				result.append(newByte);
			}
		}
		return result.toString().toUpperCase();
	}

	// Method to convert string input to byte[][] for use in mixcolumns
	private static byte[][] toByteArray(String input) {
		byte[][] result = new byte[4][4];
		String[][] resultChars = new String[4][4];
		String curString = input;
		int index = 0;
		for (int i = 0; i < curString.length(); i += 2) {
			int x = Integer.parseInt("" + curString.charAt(i), 16);
			int y = Integer.parseInt("" + curString.charAt(i + 1), 16);
			String binaryString = padBin(Integer.toBinaryString(x)) + padBin(Integer.toBinaryString(y));
			result[index][i / 8] = (byte) Integer.parseInt(binaryString, 2);
			resultChars[index][i / 8] = binaryString + " " + curString.substring(i, i + 2);
			index = (index + 1) % 4;
		}
		return result;
	}

	// Helper method to transpose byte array. Useful for debug
	private static void transpose(byte[][] result) {
		for (int i = 0; i < result.length; i++) {
			for (int j = i; j < result[0].length; j++) {
				byte temp = result[i][j];
				result[i][j] = result[j][i];
				result[j][i] = temp;
			}
		}
	}

	// Pads binary text of hexidecimal byte appropriately
	private static String padBin(String binaryString) {
		String result = binaryString;
		int len = binaryString.length();
		int padLen = 4 - len;
		for (int i = 0; i < padLen; i++) {
			result = "0" + result;
		}
		return result;
	}

	// Method for shifting the rows in the AES algorithm. Shifts differently for each row in the string
	private static String shiftRows(String input) {
		String row1 = input.substring(0, 8);
		String row2 = input.substring(8, 16);
		String row3 = input.substring(16, 24);
		String row4 = input.substring(24);
		StringBuilder result = new StringBuilder();
		String[] rows = { row1, row2, row3, row4 };
		for (int i = 0; i < 4; i++) {
			result.append(rows[i].substring(0, 2));
			result.append(rows[(i + 1) % 4].substring(2, 4));
			result.append(rows[(i + 2) % 4].substring(4, 6));
			result.append(rows[(i + 3) % 4].substring(6));
		}
		return result.toString().toUpperCase();
	}

	// Inverse Method for shifting the rows in the AES algorithm. Shifts differently for each row in the string
	private static String invShiftRows(String input) {
		String row1 = input.substring(0, 8);
		String row2 = input.substring(8, 16);
		String row3 = input.substring(16, 24);
		String row4 = input.substring(24);
		StringBuilder result = new StringBuilder();
		String[] rows = { row1, row2, row3, row4 };
		for (int i = 0; i < 4; i++) {
			result.append(rows[i].substring(0, 2));
			result.append(rows[(i + 3) % 4].substring(2, 4));
			result.append(rows[(i + 2) % 4].substring(4, 6));
			result.append(rows[(i + 1) % 4].substring(6));
		}
		return result.toString().toUpperCase();
	}

	// SubBytes method for AES. Looks up using the hexidecimal digits in the sBox appropriately and 
	// reassigns the data.
	private static String subBytes(String input) {
		StringBuilder result = new StringBuilder();
		String curString = input;
		for (int i = 0; i < curString.length() - 1; i += 2) {
			int x = Integer.parseInt("" + curString.charAt(i), 16);
			int y = Integer.parseInt("" + curString.charAt(i + 1), 16);
			String hex = decToHex(sBox[x][y]);
			result.append(hex);
		}
		return result.toString();
	}

	// Inverse subBytes method for AES. Looks up using the hexidecimal digits in the sBox appropriately and 
	// reassigns the data.
	private static String invSubBytes(String input) {
		StringBuilder result = new StringBuilder();
		String curString = input;
		for (int i = 0; i < curString.length() - 1; i += 2) {
			int x = Integer.parseInt("" + curString.charAt(i), 16);
			int y = Integer.parseInt("" + curString.charAt(i + 1), 16);
			String hex = decToHex(iSBox[x][y]);
			result.append(hex);
		}
		return result.toString();
	}

	// Convert a decimal to Hex
	private static String decToHex(int i) {
		String[] hexVal = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F" };
		String result = "";
		if (i >= 16) {
			result += "" + hexVal[i / 16];
			i = i % 16;
		} else {
			result += "0";
		}
		result += hexVal[i];
		return result;
	}

	//////////////////////// the mixColumns Tranformation //////////////////////// ////////////////////////

	final static int[] LogTable = { 0, 0, 25, 1, 50, 2, 26, 198, 75, 199, 27, 104, 51, 238, 223, 3, 100, 4, 224, 14, 52,
			141, 129, 239, 76, 113, 8, 200, 248, 105, 28, 193, 125, 194, 29, 181, 249, 185, 39, 106, 77, 228, 166, 114,
			154, 201, 9, 120, 101, 47, 138, 5, 33, 15, 225, 36, 18, 240, 130, 69, 53, 147, 218, 142, 150, 143, 219, 189,
			54, 208, 206, 148, 19, 92, 210, 241, 64, 70, 131, 56, 102, 221, 253, 48, 191, 6, 139, 98, 179, 37, 226, 152,
			34, 136, 145, 16, 126, 110, 72, 195, 163, 182, 30, 66, 58, 107, 40, 84, 250, 133, 61, 186, 43, 121, 10, 21,
			155, 159, 94, 202, 78, 212, 172, 229, 243, 115, 167, 87, 175, 88, 168, 80, 244, 234, 214, 116, 79, 174, 233,
			213, 231, 230, 173, 232, 44, 215, 117, 122, 235, 22, 11, 245, 89, 203, 95, 176, 156, 169, 81, 160, 127, 12,
			246, 111, 23, 196, 73, 236, 216, 67, 31, 45, 164, 118, 123, 183, 204, 187, 62, 90, 251, 96, 177, 134, 59,
			82, 161, 108, 170, 85, 41, 157, 151, 178, 135, 144, 97, 190, 220, 252, 188, 149, 207, 205, 55, 63, 91, 209,
			83, 57, 132, 60, 65, 162, 109, 71, 20, 42, 158, 93, 86, 242, 211, 171, 68, 17, 146, 217, 35, 32, 46, 137,
			180, 124, 184, 38, 119, 153, 227, 165, 103, 74, 237, 222, 197, 49, 254, 24, 13, 99, 140, 128, 192, 247, 112,
			7 };

	final static int[] AlogTable = { 1, 3, 5, 15, 17, 51, 85, 255, 26, 46, 114, 150, 161, 248, 19, 53, 95, 225, 56, 72,
			216, 115, 149, 164, 247, 2, 6, 10, 30, 34, 102, 170, 229, 52, 92, 228, 55, 89, 235, 38, 106, 190, 217, 112,
			144, 171, 230, 49, 83, 245, 4, 12, 20, 60, 68, 204, 79, 209, 104, 184, 211, 110, 178, 205, 76, 212, 103,
			169, 224, 59, 77, 215, 98, 166, 241, 8, 24, 40, 120, 136, 131, 158, 185, 208, 107, 189, 220, 127, 129, 152,
			179, 206, 73, 219, 118, 154, 181, 196, 87, 249, 16, 48, 80, 240, 11, 29, 39, 105, 187, 214, 97, 163, 254,
			25, 43, 125, 135, 146, 173, 236, 47, 113, 147, 174, 233, 32, 96, 160, 251, 22, 58, 78, 210, 109, 183, 194,
			93, 231, 50, 86, 250, 21, 63, 65, 195, 94, 226, 61, 71, 201, 64, 192, 91, 237, 44, 116, 156, 191, 218, 117,
			159, 186, 213, 100, 172, 239, 42, 126, 130, 157, 188, 223, 122, 142, 137, 128, 155, 182, 193, 88, 232, 35,
			101, 175, 234, 37, 111, 177, 200, 67, 197, 84, 252, 31, 33, 99, 165, 244, 7, 9, 27, 45, 119, 153, 176, 203,
			70, 202, 69, 207, 74, 222, 121, 139, 134, 145, 168, 227, 62, 66, 198, 81, 243, 14, 18, 54, 90, 238, 41, 123,
			141, 140, 143, 138, 133, 148, 167, 242, 13, 23, 57, 75, 221, 124, 132, 151, 162, 253, 28, 36, 108, 180, 199,
			82, 246, 1 };

	private static byte mul(int a, byte b) {
		int inda = (a < 0) ? (a + 256) : a;
		int indb = (b < 0) ? (b + 256) : b;

		if ((a != 0) && (b != 0)) {
			int index = (LogTable[inda] + LogTable[indb]);
			byte val = (byte) (AlogTable[index % 255]);
			return val;
		} else
			return 0;
	} // mul

	// In the following two methods, the input c is the column number in
	// your evolving state matrix st (which originally contained
	// the plaintext input but is being modified). Notice that the state here is
	// defined as an
	// array of bytes. If your state is an array of integers, you'll have
	// to make adjustments.

	public static void mixColumn2(int c, byte[][] st) {
		// This is another alternate version of mixColumn, using the
		// logtables to do the computation.

		byte a[] = new byte[4];

		// note that a is just a copy of st[.][c]
		for (int i = 0; i < 4; i++)
			a[i] = st[i][c];

		// This is exactly the same as mixColumns1, if
		// the mul columns somehow match the b columns there.
		st[0][c] = (byte) (mul(2, a[0]) ^ a[2] ^ a[3] ^ mul(3, a[1]));
		st[1][c] = (byte) (mul(2, a[1]) ^ a[3] ^ a[0] ^ mul(3, a[2]));
		st[2][c] = (byte) (mul(2, a[2]) ^ a[0] ^ a[1] ^ mul(3, a[3]));
		st[3][c] = (byte) (mul(2, a[3]) ^ a[1] ^ a[2] ^ mul(3, a[0]));
	} // mixColumn2

	public static void invMixColumn2(int c, byte[][] st) {
		byte a[] = new byte[4];

		// note that a is just a copy of st[.][c]
		for (int i = 0; i < 4; i++)
			a[i] = st[i][c];

		st[0][c] = (byte) (mul(0xE, a[0]) ^ mul(0xB, a[1]) ^ mul(0xD, a[2]) ^ mul(0x9, a[3]));
		st[1][c] = (byte) (mul(0xE, a[1]) ^ mul(0xB, a[2]) ^ mul(0xD, a[3]) ^ mul(0x9, a[0]));
		st[2][c] = (byte) (mul(0xE, a[2]) ^ mul(0xB, a[3]) ^ mul(0xD, a[0]) ^ mul(0x9, a[1]));
		st[3][c] = (byte) (mul(0xE, a[3]) ^ mul(0xB, a[0]) ^ mul(0xD, a[1]) ^ mul(0x9, a[2]));
	} // invMixColumn2
}

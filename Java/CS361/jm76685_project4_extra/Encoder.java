import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.PriorityQueue;
/*
 * In Encoder.java, The most important methods are decodeFile and encodeFile. The method decodeFile
 * uses the mappings of encryptions to characters to interpret the file one line at a time. The method encodeFile uses the 
 * mappings of characters to encyptions to write out a file of encodings. All of the other methods are for creating the huffman
 * codes used for the mappings or for generating a random string of text.
 * 
 * Credit to http://cs.smith.edu/dftwiki/index.php/CSC212_Huffman_Ecoding_in_Java 
 * Website used for getting the huffman codes algorithm. 
 */

public class Encoder {
	public static final int NUM_LETTERS = 500;
	public static final int ALPHABET_SIZE = 26;

	// Run arguments: java Encoder frequenciesFile k
	public static void main(String[] args) throws NumberFormatException, IOException {
		String fileName = "";
		int numIntegers = 0;
		int numSymbols = 0;
		boolean useFile = false;
		String newFileName = "";
		// This conditional section is used to interpret the command line
		// arguments and
		// extract the correct file name. Also extracts the number of integers
		// to interpret
		if (args.length == 2) {
			if (args[0].equals("frequenciesFile")) {
				try {
					numIntegers = Integer.parseInt(args[1]);
				} catch (NumberFormatException e) {
					System.err.println("Error in arguments");
					System.exit(1);
				}
			} else {
				System.err.println("Error in arguments");
				System.exit(1);
			}
			fileName = args[0];
		} else {
			if (args.length == 3){
				if (args[0].equals("frequenciesFile")) {
					try {
						numIntegers = Integer.parseInt(args[1]);
						numSymbols = Integer.parseInt(args[2]);
					} catch (NumberFormatException e) {
						System.err.println("Error in arguments 1");
						System.exit(1);
					}
				} else {
					System.err.println("Error in arguments 2");
					System.exit(1);
				}
				fileName = args[0];
			}
			else {
				if (args.length == 4){
					if (args[0].equals("frequenciesFile")) {
						try {
							numIntegers = Integer.parseInt(args[1]);
							numSymbols = Integer.parseInt(args[2]);
							useFile = true;
							newFileName = args[3];
							
						} catch (NumberFormatException e) {
							System.err.println("Error in arguments 1");
							System.exit(1);
						}
					} else {
						System.err.println("Error in arguments 2");
						System.exit(1);
					}
					fileName = args[0];
				}
				else {
					System.err.println("Error in arguments 3 ");
					System.exit(1);
				}
			}
		}

		// These next few lines of code read the file based on the file name and
		// initialize the Input/Output
		// Streams that will be used in transferring the data
		File file = new File(fileName);
		FileReader fileReader = new FileReader(file);
		BufferedReader br = new BufferedReader(fileReader);

		int sum = 0;
		int[] frequencies = new int[ALPHABET_SIZE];
		HashMap<String, Integer> freqs = new HashMap<String, Integer>();
		
		
		// UnComment this out to use the frequency file of outside source
		if (useFile){
			sum = readFileFreq(freqs, frequencies, newFileName);
			numIntegers = ALPHABET_SIZE;
		}
		else {
			// Parsing of the file of the frequencies. Also calulates total sum to
			// be used in probabilities.
			for (int i = 0; i < numIntegers; i++) {
				int lineNum = Integer.parseInt(br.readLine());
				sum += lineNum;
				frequencies[i] = lineNum;
				freqs.put("" + (char) (i + 'A'), lineNum);
			}
		}

		double entropy = 0;
		double[] ranges = new double[ALPHABET_SIZE];
		double rangeTop = 0;
		int index = 0;
		// Calculates entropy and also the ranges to be used in generating the
		// random file of characters
		for (int i : frequencies) {
			if (i == 0)
				break;
			double freq = i;
			double probability = freq / sum;
			entropy += -1 * (probability * log(probability, 2));
			rangeTop += probability;
			ranges[index] = rangeTop;
			index++;
		}
		System.out.println("Entropy: " + entropy);

		// deque from priority que into a map of the encodings
		// Encodes a file using only one symbol.
		encoderFunction(1, numIntegers, entropy, frequencies, newFileName);

		// Encodes a file using any number of symbols.
		encoderFunction(numSymbols, numIntegers, entropy, frequencies, newFileName);
		br.close();
	}

	// compute the probabilities of characters (in the text) ignoring any non-letters and ignoring case. 
	private static int readFileFreq(HashMap<String, Integer> freqs, int[] frequencies, String newFileName) throws IOException {
		int sum = 0;
		String fileName = newFileName;
		File file = new File(fileName);
		FileReader fileReader = new FileReader(file);
		BufferedReader br = new BufferedReader(fileReader);
		String curString = br.readLine();
		while (curString != null){
			curString = onlyChars(curString);
			for (char c: curString.toCharArray()){
				sum++;
				frequencies[c - 'A']++;
				freqs.put("" + c, frequencies[c - 'A']);
			}
			curString = br.readLine();
		}
		printFrequencies(frequencies);
		return sum;
	}
	
	// utility to print out the frequencies
	private static void printFrequencies(int[] frequencies) {
		System.out.println("Frequencies: ");
		for (int i = 0; i < ALPHABET_SIZE; i++){
			System.out.println("Frequency of " + (char)('A' + i) + " is :" + frequencies[i]);
		}
	}

	private static String onlyChars(String curString) {
		if (curString == null)
			return null;
		StringBuilder result = new StringBuilder();
		curString = curString.toUpperCase();
		for (int i = 0; i < curString.length(); i++){
			char curChar = curString.charAt(i);
			if (curChar <= 'Z' && curChar >= 'A')
				result.append(curChar);
		}
		return result.toString();
	}

	// Extra Credit Method. Encodes a file of any arbitrary number of symbols. 
	private static void encoderFunction(int numSymbols, int numIntegers, double entropy, int[] frequencies, String fName) throws IOException {
		System.out.println("\n" + numSymbols + " symbol Encodings");
		HashMap<String, String> decodes = new HashMap<String, String>();
		HashMap<String, Integer> freqs = new HashMap<String, Integer>();
		for (int i = 0; i < numIntegers; i++){
			addToFreqs(freqs, frequencies[i], numSymbols - 1, "" + (char) (i + 'A'), numIntegers, frequencies);
		}
		
		Node treeHead2 = buildHuffmanTree(freqs);
		HashMap<String, String> codes = getEncoding(treeHead2);
		for (String s : codes.keySet()) {
			System.out.println(s + " " + codes.get(s));
			decodes.put(codes.get(s), s);
		}
		double bitAvg = encodeFile(codes, "testText.enc" + numSymbols, numSymbols, fName);
		double efficiency = bitAvg / entropy;
		decodeFile(decodes, "testText.enc" + numSymbols, "testText.dec" + numSymbols, numSymbols);
		System.out.println("\nEfficiency" + numSymbols + ": " + efficiency + "  bitAvg: " + bitAvg);
	}

	// Recursive method to generate the frequency map to use for generating the huffman tree
	private static void addToFreqs(HashMap<String, Integer> freqs, int value, int numSymbols, String mess, int numIntegers, int[] freq) {
		if (numSymbols == 0){
			freqs.put(mess, value);
		}
		else {
			for (int i = 0; i < numIntegers; i++){
				addToFreqs(freqs, value + freq[i], numSymbols - 1, mess + (char) (i + 'A'), numIntegers, freq);
			}
		}	
	}

	/*
	 * Main method to decode the file. Uses the mappings of the huffman code to
	 * the original character to output the result.
	 */
	private static void decodeFile(HashMap<String, String> decodes, String inputName, String outputName, int size)
			throws IOException {
		String fileName = inputName;
		File file = new File(fileName);
		FileReader fileReader = new FileReader(file);
		BufferedReader br = new BufferedReader(fileReader);
		StringBuilder output = new StringBuilder();
		for (int i = 0; i < NUM_LETTERS; i++) {
			String text = br.readLine();
			output.append(decodes.get(text));
		}
		BufferedWriter writer = new BufferedWriter(new FileWriter(outputName));
		writer.write(output.toString());
		writer.close();
		br.close();
	}

	/*
	 * Main method to encode the file. Uses the mappings of the original
	 * character to the huffman code to output the result.
	 */
	private static double encodeFile(HashMap<String, String> codes, String outputFileName, int size, String fName)
			throws IOException {
		double result = 0;
		String fileName = fName;
		boolean isFile = false;
		if (fName.equals("")){
			fileName = "testText";
		}
		else {
			isFile = true;
		}
			
		File file = new File(fileName);
		FileReader fileReader = new FileReader(file);
		BufferedReader br = new BufferedReader(fileReader);
		String text = onlyChars(br.readLine());
		StringBuilder output = new StringBuilder();
		int len = 0;
		while (isFile && text != null){
			len += text.length();
			for (int i = 0; i < text.length() - size; i += size) {
				String temp = "";
				for (int j = 0; j < size; j++) {
					temp += text.charAt(i + j);
				}
				//System.out.println(temp);
				String val = codes.get(temp);
				output.append(val + "\n");
				result += val.length();
			}
			text = onlyChars(br.readLine());
		}
		BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName));
		writer.write(output.toString());
		writer.close();
		br.close();
		return result / (1.0 * len);
	}

	/*
	 * Generates a file of size NUM_LETTERS, using probabilities of how frequent
	 * the character is to generate the letters
	 */
	private static void generateFile(double[] ranges) throws IOException {
		StringBuilder totalFile = new StringBuilder();
		for (int i = 0; i < NUM_LETTERS; i++) {
			double num = Math.random();
			char index = (char) ('A' + getIndex(num, ranges));
			totalFile.append(index);
		}
		BufferedWriter writer = new BufferedWriter(new FileWriter("testText"));
		writer.write(totalFile.toString());
		writer.close();
	}

	/*
	 * Gets the index based on the randomly generated number.
	 */
	private static int getIndex(double num, double[] ranges) {
		for (int i = 0; i < ranges.length; i++) {
			if (ranges[i] > num)
				return i;
		}
		return 0;
	}

	// Credit to
	// http://cs.smith.edu/dftwiki/index.php/CSC212_Huffman_Ecoding_in_Java
	private static HashMap<String, String> getEncoding(Node root) {
		HashMap<String, String> encoding = new HashMap<String, String>();
		DFS(root, "", encoding);
		return encoding;
	}

	// Credit to
	// http://cs.smith.edu/dftwiki/index.php/CSC212_Huffman_Ecoding_in_Java
	private static void DFS(Node node, String code, HashMap<String, String> encoding) {
		if (node.isLeaf())
			encoding.put(node.letters, code);
		else {
			if (node.left != null)
				DFS(node.left, code + "0", encoding);
			if (node.right != null)
				DFS(node.right, code + "1", encoding);
		}
	}

	// Credit to
	// http://cs.smith.edu/dftwiki/index.php/CSC212_Huffman_Ecoding_in_Java
	private static Node buildHuffmanTree(HashMap<String, Integer> freqs) {
		PriorityQueue<Node> prioQ = new PriorityQueue<Node>();
		for (String s : freqs.keySet())
			prioQ.add(new Node(s, freqs.get(s), null, null));

		while (prioQ.size() > 1) {
			Node left = prioQ.poll();
			Node right = prioQ.poll();
			prioQ.add(new Node("#", left.freq + right.freq, left, right));
		}

		return prioQ.poll();
	}

	// Utility to calulate log base x of a number
	private static double log(double num, int base) {
		return Math.log(num) / Math.log(base);
	}

}

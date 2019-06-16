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
			System.err.println("Error in arguments");
			System.exit(1);
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
		// Parsing of the file of the frequencies. Also calulates total sum to
		// be used in probabilities.
		for (int i = 0; i < numIntegers; i++) {
			int lineNum = Integer.parseInt(br.readLine());
			sum += lineNum;
			frequencies[i] = lineNum;
			freqs.put("" + (char) (i + 'A'), lineNum);
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
		System.out.println("\nEncodings");
		HashMap<String, String> decodes = new HashMap<String, String>();
		Node treeHead = buildHuffmanTree(freqs);
		HashMap<String, String> codes = getEncoding(treeHead);
		for (String s : codes.keySet()) {
			System.out.println(s + " " + codes.get(s));
			decodes.put(codes.get(s), s);
		}

		generateFile(ranges);
		double bitAvg = encodeFile(codes, "testText.enc1", 1);
		double efficiency = bitAvg / entropy;
		decodeFile(decodes, "testText.enc1", "testText.dec1", 1);
		System.out.println("\nEfficiency: " + efficiency + "  bitAvg: " + bitAvg);

		// Encodes a file using two symbol.
		System.out.println("\n2 symbol Encodings");
		HashMap<String, String> decodes2 = new HashMap<String, String>();
		HashMap<String, Integer> freqs2 = new HashMap<String, Integer>();
		for (int i = 0; i < numIntegers; i++) {
			for (int j = 0; j < numIntegers; j++) {
				int probability = frequencies[i] * frequencies[j];
				int value = frequencies[i] + frequencies[j];
				freqs2.put("" + (char) (i + 'A') + (char) (j + 'A'), value);
			}
		}
		Node treeHead2 = buildHuffmanTree(freqs2);
		HashMap<String, String> codes2 = getEncoding(treeHead2);
		for (String s : codes2.keySet()) {
			System.out.println(s + " " + codes2.get(s));
			decodes2.put(codes2.get(s), s);
		}

		double bitAvg2 = encodeFile(codes2, "testText.enc2", 2);
		double efficiency2 = bitAvg2 / entropy;
		decodeFile(decodes2, "testText.enc2", "testText.dec2", 2);
		System.out.println("\nEfficiency2: " + efficiency2 + "  bitAvg: " + bitAvg2);
		br.close();
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
	private static double encodeFile(HashMap<String, String> codes, String outputFileName, int size)
			throws IOException {
		double result = 0;
		String fileName = "testText";
		File file = new File(fileName);
		FileReader fileReader = new FileReader(file);
		BufferedReader br = new BufferedReader(fileReader);
		String text = br.readLine();
		StringBuilder output = new StringBuilder();
		for (int i = 0; i < text.length(); i += size) {
			String temp = "";
			for (int j = 0; j < size; j++) {
				temp += text.charAt(i + j);
			}
			String val = codes.get(temp);
			output.append(val + "\n");
			result += val.length();
		}
		BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName));
		writer.write(output.toString());
		writer.close();
		br.close();
		return result / (1.0 * text.length());
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

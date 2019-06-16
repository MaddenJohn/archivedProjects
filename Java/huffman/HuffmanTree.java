/*  Student information for assignment:
 *
 *  On our honor, Jonathan Madden and Khiem Tang, this programming assignment is our own work
 *  and we have not provided this code to any other student.
 *
 *  Number of slip days used: 1
 *
 *  Student 1: Jonathan Madden
 *  UTEID: jm76685
 *  email address: johnmadden4477@yahoo.com
 *  Grader name: Donghyuk
 *  Section number: 51740
 *
 *  Student 2: Khiem Tang
 *  UTEID: klt2399
 *  email address: tang.khiem@yahoo.com
 *  Grader name: Donghyuk
 *  Section number: 51740
 */

import java.io.IOException;
import java.util.HashMap;

public class HuffmanTree {
	// Instance variables
	private TreeNode root;
	private HashMap<Integer, String> map;
	private int original;
	private int size;
	private int[] counts;

	// HuffMan tree constructor to create initial priorityQueue and tree from queue
	public HuffmanTree(BitInputStream bits) throws IOException {
		// Defines counts int array to create frequencies
		counts = letterCount(bits);
		// Creates priority queue from frequency array
		PriorityQueue<TreeNode> queue = createQueue(counts);
		size = queue.size() * 10;
		// Creates tree from queue
		createTree(queue);
		map = new HashMap<Integer, String>();
		root = queue.front();
		// Creates map of integer/string based on queue root
		createMap(map, root, "");
	}

	// HuffMan tree constructor for decompression:
	// Creates tree for use in making the standard count format tree for decompressing
	public HuffmanTree(int[] otherCounts) {
		this.counts = otherCounts;
		// Creates queue based on counts frequency array
		PriorityQueue<TreeNode> queue = createQueue(counts);
		// Creates tree based on the mapped priority queue
		size = queue.size();
		createTree(queue);
		map = new HashMap<Integer, String>();
		root = queue.front();
		// Creates map of integer/string based on queue root
		createMap(map, root, "");
	}

	// HuffMan tree constructor for decompression:
	// Creates tree for use in making the standard tree format tree for decompressing
	public HuffmanTree(int tgtSize, BitInputStream bits) throws IOException {
		// Size condition with tgtSize, passed in from decompress call
		if (tgtSize>0) {
			size=tgtSize;
			// Reads the next bit
			int bit = bits.readBits(1);
			// Sets root to new node, initiate recursive method
			root = new TreeNode(bit, getChild(bits), getChild(bits));
		}
	}

	// Helper method getChild to create node / leaf and place in data
	private TreeNode getChild(BitInputStream bits)
			throws IOException {
		// Defines bit as the next bit
		int bit = bits.readBits(1);
		TreeNode result;
		// If node is found, make node and continue recursive call
		if (bit == 0) {
			result = new TreeNode(bit, getChild(bits), getChild(bits));
			// If leaf is found
		} else {
			// Create new TreeNode with value of next 9 bits
			int value = bits.readBits(1 + IHuffConstants.BITS_PER_WORD);
			result = new TreeNode(value, 1);
		}
		return result;
	}

	// getMap method to return hashMap
	public HashMap<Integer, String> getMap() {
		return map;
	}

	// getRoot method to return root
	public TreeNode getRoot() {
		return root;
	}

	// getOriginal method to obtain original file size
	public int getOriginal() {
		return original;
	}

	// getSize method to return size
	public int getSize() {
		return size;
	}

	// getCounts method to return frequency array
	public int[] getCounts() {
		return counts;
	}

	// getSaved helper method to calculate compressed file size
	public int getSaved(int headerFormat) {
		// Defines letters as the frequency array
		int[] letters = getCounts();
		// Define codes as map of tree bits
		HashMap<Integer, String> codes = getMap();
		int afterCompress = 0;
		// Increment afterCompress variable with header and magic number
		afterCompress += IHuffConstants.BITS_PER_INT * 2;
		for (int x : codes.keySet()) {
			// Increments codes, including psuedo_eof
			afterCompress += codes.get(x).length() * letters[x];
		}
		// Incrementing for standard tree format
		if (headerFormat == IHuffConstants.STORE_TREE) {
			afterCompress += IHuffConstants.BITS_PER_INT; // size
			afterCompress += treeBits(getRoot());
			// Incrementing for standard count format
		} else if (headerFormat == IHuffConstants.STORE_COUNTS) {
			for (int k = 0; k < IHuffConstants.ALPH_SIZE; k++) {
				afterCompress += IHuffConstants.BITS_PER_INT;
			}
		}
		return getOriginal() - afterCompress;
	}

	// treeBits helper method to return int bit of node
	private int treeBits(TreeNode node) {
		if (node != null) {
			// If node is a leaf, return corresponding bits
			if (node.isLeaf()) {
				return 2 + IHuffConstants.BITS_PER_WORD;
			} else {
				// Else, continue traversing tree
				return 1 + treeBits(node.getLeft()) + treeBits(node.getRight());
			}
		}
		return 0;
	}

	// letterCount method for tallying letters
	private int[] letterCount(BitInputStream bits) throws IOException {
		// Define letter array with all possible character size
		int[] letters = new int[257];
		int inbits;
		// Read in bits until not possible, and tally letters
		while ((inbits = bits.readBits(IHuffConstants.BITS_PER_WORD)) != -1) {
			letters[inbits]++;
			// Increment original size variable
			original += 8;
		}
		// Increment PSUEDO_EOF index
		letters[IHuffConstants.PSEUDO_EOF]++;
		return letters;
	}

	// createQueue method to create a new priority queue
	private PriorityQueue<TreeNode> createQueue(int[] letters) {
		PriorityQueue<TreeNode> counts = new PriorityQueue<TreeNode>();
		// runs through frequency array
		for (int x = 0; x < letters.length; x++) {
			if (letters[x] != 0) {
				// Enqueues when there is a visible character
				counts.enqueue(new TreeNode(x, letters[x]));
			}
		}
		return counts;
	}

	// createTree method to create tree from priority queue
	private void createTree(PriorityQueue<TreeNode> counts) {
		while (counts.size() > 1) {
			// While size > 1 of priorityQueue, dequeue twice
			TreeNode temp1 = counts.dequeue();
			TreeNode temp2 = counts.dequeue();
			// Add a new node with corresponding value
			TreeNode freq = new TreeNode(temp1.getValue() + temp2.getValue(),
					temp1, temp2);
			// Enqueue back into priorityQueue in correct position
			counts.enqueue(freq);
			size++;
		}
	}

	// createMap method to create map
	private void createMap(HashMap<Integer, String> map, TreeNode n,
			String result) {
		// if node is a leaf, put into HashMap
		if (n.isLeaf()) {
			map.put(n.getValue(), result);
			// Else, continue traversing while adding node bit to result
		} else {
			createMap(map, n.getLeft(), result + "0");
			createMap(map, n.getRight(), result + "1");
		}
	}

	// printMap method to output map
	public void printMap() {
		System.out.println("map: ");
		for (int x : map.keySet()) {
			System.out.println((char) x + " " + map.get(x));
		}
		System.out.println();
	}

}

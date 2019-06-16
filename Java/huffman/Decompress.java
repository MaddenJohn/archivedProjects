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

public class Decompress {
	// Instance variables
	private int saved;

	// DeCompress constructor (after magicNumber is checked)
	public Decompress(BitInputStream in, BitOutputStream out)
			throws IOException {
		// Defines headerFormat for creation of tree
		int headerFormat = in.readBits(IHuffConstants.BITS_PER_INT);
		// Defines new HuffManTree object for decompression
		HuffmanTree tree = createTree(in, headerFormat);
		if (tree != null) {
			writeLetters(in, out, tree.getRoot());
		}
	}

	// createTree method to decompress file based on format
	private HuffmanTree createTree(BitInputStream in, int headerFormat)
			throws IOException {
		// For Standard Count Format
		if (headerFormat == IHuffConstants.STORE_COUNTS) {
			// Define counts array for all available characters
			int[] counts = new int[257];
			for (int k = 0; k < IHuffConstants.ALPH_SIZE; k++) {
				// Cycle through ALPH_SIZE and read in bits from file for array
				counts[k] = in.readBits(IHuffConstants.BITS_PER_INT);
			}
			// Increment the counts index for PSUEDO_EOF
			counts[IHuffConstants.PSEUDO_EOF]++;
			// Returns tree
			return new HuffmanTree(counts);
			// For Standard Tree Format
		} else if (headerFormat == IHuffConstants.STORE_TREE) {
			// Read in bits from file to define size
			int size = in.readBits(IHuffConstants.BITS_PER_INT);
			// Returns tree
			return new HuffmanTree(size, in);
		}
		return null;
	}

	// getSaved method to return integer saved for output
	public int getSaved() {
		return saved;
	}

	// writeLetters method:
	// stops when it reads the Pseudo EOF character, base case: when node = leaf
	private void writeLetters(BitInputStream in, BitOutputStream out,
			TreeNode root) throws IOException {
		// Define boolean for tracking
		boolean done = false;
		TreeNode node = root;
		while (!done) {
			// When node is a leaf and is PSUEDO_EOF, completed tracking
			if (node.isLeaf()) {
				if (node.getValue() == IHuffConstants.PSEUDO_EOF) {
					done = true;
				} else {
					// Write node's value and increment saved
					out.write(node.getValue());
					// Set node to root
					node = root;
					saved += IHuffConstants.BITS_PER_WORD;
				}
			} else {
				// Read in next bit and continue traversing tree
				int bit = in.readBits(1);
				if (bit == 0) {
					node = node.getLeft();
				} else if (bit == 1) {
					node = node.getRight();
				}
				// If bit is not possible, present error
				else if (bit == -1) {
					throw new IOException(
							"Error reading compressed file. \n"
									+ "unexpected end of input. No PSEUDO_EOF character.");
				}
			}

		}
	}
}

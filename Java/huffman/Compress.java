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

public class Compress {
	// Instance variables
	private int bitsSaved;

	// Compress constructor
	public Compress(BitInputStream bits, BitOutputStream output,
			int headerFormat, HuffmanTree tree) throws IOException {
		// Writes out magicNumber and headerFormat to file
		write32Bit(output, IHuffConstants.MAGIC_NUMBER);
		write32Bit(output, headerFormat);
		// Writes compressed tree based on STF or SCF
		writeTree(output, headerFormat, tree.getCounts(), tree);
		// Writes condensed bits based on tree's map string
		writeCodes(bits, output, tree.getMap());
		// Writes PSUEDO_EOF numbers
		String code = tree.getMap().get(IHuffConstants.PSEUDO_EOF);
		output.writeBits(code.length(), Integer.parseInt(code, 2));
		// Increments bitsSaved variable from code
		bitsSaved += code.length();
		output.flush();
	}

	// writeTree method to create the compressed tree based on STF or SCF
	private void writeTree(BitOutputStream output, int headerFormat,
			int[] myCounts, HuffmanTree tree) {
		// For Standard Tree Format
		if (headerFormat == IHuffConstants.STORE_TREE) {
			// writes out bits to file and calls writeTreeHelper
			output.writeBits(IHuffConstants.BITS_PER_INT, tree.getSize());
			bitsSaved += IHuffConstants.BITS_PER_INT;
			writeTreeHelper(output, tree.getRoot());
			// For Standard Count Format
		} else if (headerFormat == IHuffConstants.STORE_COUNTS) {
			// Cycles through ALPH_SIZE and writes out frequencies
			for (int k = 0; k < IHuffConstants.ALPH_SIZE; k++) {
				output.writeBits(IHuffConstants.BITS_PER_INT, myCounts[k]);
				bitsSaved += IHuffConstants.BITS_PER_INT;
			}
		}
	}

	// writeTreeHelper method to write tree to file
	private void writeTreeHelper(BitOutputStream output, TreeNode node) {
		if (node != null) {
			// While node is not empty and is a leaf
			if (node.isLeaf()) {
				// Writes out corresponding bit value and increments bitsSaved
				// accordingly
				output.writeBits(1, 1);
				output.writeBits(IHuffConstants.BITS_PER_WORD + 1,
						node.getValue());
				bitsSaved += 1 + IHuffConstants.BITS_PER_WORD + 1;
			} else {
				// If not a leaf, traverses down tree while going through bits
				output.writeBits(1, 0);
				bitsSaved += 1;
				writeTreeHelper(output, node.getLeft());
				writeTreeHelper(output, node.getRight());
			}
		}
	}

	// writeCodes method to get specific compressed bit string needed
	private void writeCodes(BitInputStream bits, BitOutputStream output,
			HashMap<Integer, String> codes) throws IOException {
		int inbits;
		// While readBits != -1, write out parsed code string
		while ((inbits = bits.readBits(IHuffConstants.BITS_PER_WORD)) != -1) {
			String code = codes.get(inbits);
			output.writeBits(code.length(), Integer.parseInt(code, 2));
			// Increments bitsSaved based on code
			bitsSaved += code.length();
		}
	}

	// write32Bit method to write bits based on inputted constant
	private void write32Bit(BitOutputStream output, int constant) {
		output.writeBits(IHuffConstants.BITS_PER_INT, constant);
		bitsSaved += IHuffConstants.BITS_PER_INT;
	}

	// getChange method to return bitsSaved variable for output
	public int getChange() {
		return bitsSaved;
	}

}

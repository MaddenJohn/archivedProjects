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
import java.io.InputStream;
import java.io.OutputStream;

public class SimpleHuffProcessor implements IHuffProcessor {

	// Instance variables
	private IHuffViewer myViewer;
	private int header;
	private HuffmanTree tree;

	// Compress method for file compression and output
	public int compress(InputStream in, OutputStream out, boolean force)
			throws IOException {
		// Force compression error call
		if (!force && tree.getSaved(header) < 0) {
			myViewer.showError("Compressed File too big. Select Force Compression");
			return 0;
		}
		// Defines new compress object to compress / write file
		Compress compress = new Compress(new BitInputStream(in),
				new BitOutputStream(out), header, tree);
		int afterCompress = compress.getChange();
		// Returns after compress amount from compress.getChange
		showString("Compress: " + afterCompress);
		return afterCompress;
	}

	// PreprocessCompress method for file preparation
	public int preprocessCompress(InputStream in, int headerFormat)
			throws IOException {
		header = headerFormat;
		// Defines tree to create initial priority queue and tree
		tree = new HuffmanTree(new BitInputStream(in));
		// Defines integer from free to get bytes saved
		int saved = tree.getSaved(headerFormat);
		showString("preCompress: " + saved);
		return saved;
	}

	// setViewer method for defining output
	public void setViewer(IHuffViewer viewer) {
		myViewer = viewer;
	}

	// uncompress method for file decompression and output
	public int uncompress(InputStream in, OutputStream out) throws IOException {
		BitInputStream bis = new BitInputStream(in);
		// Defines magic number by reading first 32 bits
		int magic = bis.readBits(BITS_PER_INT);
		// Compares if magic number matches, if not displays error
		if (magic != MAGIC_NUMBER) {
			myViewer.showError("Error reading compressed file. \n"
					+ "File did not start with the huff magic number.");
			return -1;
		}
		// Magic number matched, creates new decompress Object to decompress
		// file
		Decompress decompress = new Decompress(new BitInputStream(in),
				new BitOutputStream(out));
		// Returns decompressed bytes amount
		showString("uncompress: " + decompress.getSaved());
		return decompress.getSaved();
	}

	// showString method for outputting results
	private void showString(String s) {
		// Updates myViewer
		if (myViewer != null) {
			myViewer.update(s);
		}
	}
}

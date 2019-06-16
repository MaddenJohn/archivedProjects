import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
/*
 * This is the main driving class for the project two of the class. This class involves
 * the creation of the subjects, the extraction of the arguments, the reading of the file, 
 * the sending of bits from the high level subject and low level subject over the covert channel, 
 * and the final output of the resulting file.
 */
public class CovertChannel {

	public static void main(String[] args) throws IOException {
		SecureSystem sys = new SecureSystem();
		int low  = SecurityLevel.LOW;
		int high = SecurityLevel.HIGH;
		boolean isVerbose = false;
		ByteArrayOutputStream output = new ByteArrayOutputStream();

		sys.createSubject("lyle", low, output);
		sys.createSubject("hal", high);
		
		String fileName = "";
		// This conditional section is used to interpret the command line arguments and
		// extract the correct file name. This assumes that a file name of "v" is not used
		// and that the characters are standard ASCII
		if(args.length > 0){
			int start = 0;
			if(args[0].equals("v")){
				start = 1;
				isVerbose = true;
			}
			for (int i = start; i < args.length; i++){
				fileName += args[i];
				if (i + 1 < args.length){
					fileName += " ";
				}
			}
		}
		// These next few lines of code read the file based on the file name and initialize the Input/Output
		// Streams that will be used in transferring the data
		File file = new File(fileName);
		int len = (int) file.length();
		String path = file.getPath();
		Path filePath = Paths.get(path);
		byte[] data = Files.readAllBytes(filePath);
		ByteArrayInputStream input = new ByteArrayInputStream(data);
		InstructionObject parse = new InstructionObject();
		ReferenceMonitor referenceMonitor = sys.getReferenceMonitor();
		referenceMonitor.setVerbose(isVerbose);
		
		int writeCount = 0;
		double start = System.currentTimeMillis();
		
		// The outer loop here will read the current bit in the ByteArrayOutputStream that will be
		// the byte to be transfered over to the lower level subject
		for (int i = 0; i < len; i++){
			int cur = input.read(); 
			covertChannelActions(getBits(cur), referenceMonitor, parse, sys);
			writeCount++;	
		}
		// Print data about this file and the bandwidth
		// System.out.println(writeCount + " bytes " + writeCount * 8.0 / (System.currentTimeMillis() - start) + " bits/ms");
		FileOutputStream myFOS = new FileOutputStream(fileName + ".out");
		output.writeTo(myFOS);
		myFOS.close();
		output.close();
		input.close();
	}
	
	/*
	 * This function combines a variety of actions in such a way as to implement a covert channel.
	 * This covert channel is done by taking advantage of the create, destroy and run operations.
	 * These actions are then stored in the resulting byte StringBuilder object, which is written
	 * to the ByteArrayOutputStream for storing the Bytes that will be written to the output file of the
	 * lower level subject. This array loops through the current byte, and should always have 8 different
	 * bits that need to go through this covert action process. The reference monitor also does not need
	 * to worry about parsing, so is set to the appropriate variables to complete this process in a much
	 * faster fashion. The actual operations of writing and storing of the resulting byte are done through the run
	 * operation of the lyle command. 
	 */
	public static void covertChannelActions(int[] curByte, ReferenceMonitor referenceMonitor, InstructionObject parse, SecureSystem sys){
		for (int x: curByte){
			if (x == 0){
				parse.setParse("create", "hal", "obj", 0);
				referenceMonitor.doAction(parse, sys.getSubjectList());
			}
			parse.setParse("create", "lyle", "obj", 0);
			referenceMonitor.doAction(parse, sys.getSubjectList());
			parse.setParse("write", "lyle", "obj", 1);
			referenceMonitor.doAction(parse, sys.getSubjectList());
			parse.setParse("read", "lyle", "obj", 0);
			referenceMonitor.doAction(parse, sys.getSubjectList());
			parse.setParse("destroy", "lyle", "obj", 0);
			referenceMonitor.doAction(parse, sys.getSubjectList());
			parse.setParse("run", "lyle", null, 0);
			referenceMonitor.doAction(parse, sys.getSubjectList());	
		}
	}
	
	// Function to get an integer array of the binary bits representing a number of size 0 - 255
	public static int[] getBits (int num){
		int[] result = new int[8];
		for (int i = 0; i < 8; i++){
			result[i] = num % 2;
			num /= 2;
		}
		for (int i = 0; i < 4; i++)
			swap(result, i, 7 - i);
		return result;
	}
	
	// Swap function to swap elements in an array. Used to reverse the array in the getBits() function
	public static void swap(int[] nums, int indexOne, int indexTwo){
		int temp = nums[indexOne];
		nums[indexOne] = nums[indexTwo];
		nums[indexTwo] = temp;
	}
	
	// Debugging function to print all the numbers stored in an array. 
	public static void printBits(int[] nums){
		for(int x: nums)
			System.out.print(x + " ");
		System.out.println();
	}

}

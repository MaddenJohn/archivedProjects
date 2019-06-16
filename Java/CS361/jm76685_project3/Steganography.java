import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.imageio.ImageIO;
/*
 * Main Java Class and only file for this project by Jonathan Madden, jm76685
 * First, the main function handles the parsing of the command line arguments, calling
 * the appropriate function based on this and printing error for invalid arguments.
 * If the readPicture function is called, then the main decoding
 * algorithm will be run. This algorithm reads each of the three rgb values 
 * for a pixel and adds these two an array of bits. This array is 
 * interpreted as 3 bytes and when filled, will write the appropriate 
 * data to be stored later for the final write to the message-out. This
 * method also checks for a zero byte and if found then the message has
 *  ended and the function will end. If the writeToPicture function is called
 * then a similar process will happen, reading the rgb values, and 
 * reading the value of the message, but this time the rgb values will be 
 * modified for a new image to be stored. This image will have updated rgb 
 * values storing the message as odd or even numbers. If the message
 * is too long, then it will be truncated and a message will be printed to console. 
 */
public class Steganography {

	/*
	 * Main method to parse command line. Exits with error code 1 if bad argument input.
	 */
	public static void main(String[] args) throws IOException {
		String imageName = "";
		String messageName = "";
		boolean isWrite = false;
		if(args.length == 3){
			if(args[0].equals("-E")){
				isWrite = true;
			}
			else if(args[0].equals("-D")){
				isWrite = false;
			}
			else {
				System.err.println("Error in arguments");
				System.exit(1);
			}
			imageName = args[1];
			messageName = args[2];
		}
		else {
			System.err.println("Error in arguments");
			System.exit(1);
		}
		
		if (isWrite){
			writeToPicture(imageName, messageName);
		}
		else {
			readPicture(imageName, messageName);
		}
		
        

    }
	
	/*
	 * Function to readAnyEncrypted picutre and decode it. First reads the image, then checks each rgb value
	 * and puts these into an array that will be used to output the message. 
	 */
	private static void readPicture(String imageName, String messageName) throws IOException {
		BufferedImage img = null;
        try {
            img = ImageIO.read(new File(imageName));
        } catch (IOException e) {
        	System.err.println("Error in imageName");
			System.exit(1);
        }
        
        int height = img.getHeight();
        int width = img.getWidth();
        // print image statistics
        System.out.println("Filename: " + imageName + "\nHeight: " + height  + "\nWidth: " +  width + "\nNumber of Pixels: " 
        + height * width);
        int len = 1000;
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        
        int x = 0;
        int y = 0;
        int byteIndex = 0;
        int[] bytePic = new int[8];
        int count = 0;
        boolean done = false;
        // Loop which checks each rgb pixel
        while (!done && y < height){
        	count+=3;
        	int rgb = img.getRGB(x, y);
        	int[] rgbArray = getRGBArray(rgb);
        	for (int num: rgbArray){
        		writeToOutput(num, output, byteIndex, bytePic);
        		done = checkDone(bytePic);
        		byteIndex = (byteIndex + 1) % 8;
        	}
        	x = (x + 1) % width;
        	if (x == 0)
				y++;
        	
        }
        // when finished write to outputstream, creating the new message
        FileOutputStream myFOS = new FileOutputStream(messageName);
		output.writeTo(myFOS);
		myFOS.close();
        output.close();
	}

	// This function returns true if the byte is not all zero and is used to check if we are done decoding a picture.
	private static boolean checkDone(int[] bytePic) {
		for (int num: bytePic)
			if (num != 0)
				return false;
		return true;
	}

	// This function writes a specific byte to the ouput.
	private static void writeToOutput(int colorNum, ByteArrayOutputStream output, int byteIndex, int[] bytePic) throws IOException {
		bytePic[byteIndex] = colorNum % 2;
		if (byteIndex == 7){
			output.write(getByte(bytePic));
		}
	}

	// This punction returns a byte based on an int[] argument, which can then be used to write to Output.
	private static byte getByte(int[] bytePic) {
		StringBuilder temp = new StringBuilder();
		for (int num: bytePic){
			temp.append(num);
		}
		byte result = Byte.parseByte(temp.toString(), 2);
		return result;
	}

	/*
	 * Function to encrypt the picture with the data. Loops through each letter in the file and 
	 * puts each bit into an rgb value in the picture.
	 */
	private static void writeToPicture(String imageName, String messageName) throws IOException {
		BufferedImage img = null;
        try {
            img = ImageIO.read(new File(imageName));
        } catch (IOException e) {
        	System.err.println("Error in imageName");
			System.exit(1);
        }
        
        int height = img.getHeight();
        int width = img.getWidth();
        // print image statistics
        System.out.println("Filename: " + imageName + "\nHeight: " + height  + "\nWidth: " +  width + "\nNumber of Pixels: " 
        + height * width);

        File file = new File(messageName);
		int len = (int) file.length();
		String path = file.getPath();
		Path filePath = Paths.get(path);
		byte[] data = Files.readAllBytes(filePath);
		ByteArrayInputStream input = new ByteArrayInputStream(data);
		ByteArrayOutputStream output = new ByteArrayOutputStream();
        
		int indexW = 0;
		int indexH = 0;
		int written = 0;
		System.out.println(len);
		int cur = input.read(); 
		// loop to do the encrypting.
        while (cur != -1){
			int[] byte1 = getBits(cur);
			cur = input.read(); 
			if (cur == -1)
				cur = 0;
			int[] byte2 = getBits(cur);
			cur = input.read(); 
			if (cur == -1)
				cur = 0;
			int[] byte3 = getBits(cur);
			int[] totalByte = getTotalByte(byte1, byte2, byte3);
			int bitModified = 0;
			// Gets the bits of 3 bytes at a time to conserve the entire bits for usage in encoding
			while (bitModified < 24 && indexH < height){
				setNewByte(img, totalByte, bitModified, indexW, indexH);
				bitModified+=3;
				indexW = (indexW + 1) % width;
				if (indexW == 0)
					indexH++;
				if (indexH == height){
					System.out.println("Message too long. Truncated message.");
				}
			}
			cur = input.read(); 
		}
        String[] split = imageName.split("\\.");
        String newImageName = split[0] + "-steg." + split[1];
        File saveFile = new File(newImageName);
        ImageIO.write(img, split[1], saveFile);
        output.close();
		input.close();
	}

	// Sets the new rgb values.
	private static void setNewByte(BufferedImage img, int[] totalByte, int indexBit, int indexW, int indexH) {
		int rgbNum = img.getRGB(indexW, indexH);
		int newRGB = newRBG(rgbNum, totalByte[indexBit], totalByte[indexBit + 1], totalByte[indexBit + 2]);
        img.setRGB(indexW, indexH, newRGB);
	}

	// returns the new rgb values based on the old rgb value and whether we want to encode an even or odd number.
	// handles outlier cases with conditionals. Uses bit shifting and masks to accomplish this.
	private static int newRBG(int rgbNum, int bitR, int bitG, int bitB) {	
		int[] rgb = getRGBArray(rgbNum);
		int[] bits = {bitR, bitG, bitB};
		for (int i = 0; i < 3; i++){
			if(rgb[i] % 2 == 0){ // color num is even
				if (bits[i] == 1){
					// add
					rgb[i] += 1;
				}
			}
			else { // color num is odd
				if (bits[i] == 0){
					// subtract
					rgb[i] -= 1;
				}
			}
		}
		int result = (255 << 24) | (rgb[0] << 16) | (rgb[1] << 8) | rgb[2];
		return result;
	}

	// This function returns an int[] holding all of the bit of 3 bytes.
	private static int[] getTotalByte(int[] byte1, int[] byte2, int[] byte3) {
		int[] totalByte = new int[24];
		for (int i = 0; i < 8; i++){
			totalByte[i] = byte1[i]; 
			totalByte[i + 8] = byte2[i]; 
			totalByte[i + 16] = byte3[i]; 
		}
		return totalByte;
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
	
	// Function to return an int[] of the rgb values, stored in 8 bit quantities.
	public static int[] getRGBArray (int num){
		int blue = 255 & num;
		int green = ((255 << 8) & num) >> 8;
		int red = ((255 << 16) & num) >> 16;
		int result[] = {red, green, blue};
		return result;
	}
	
	// Debuging fucntion to print the rgb values masked to actual 8 bit quantities.
	public static void printRGBArray (int num){
		int blue = 255 & num;
		int green = ((255 << 8) & num) >> 8;
		int red = ((255 << 16) & num) >> 16;
		System.out.println("RGB: "+ red + " " + green + " " + blue);
	}
}

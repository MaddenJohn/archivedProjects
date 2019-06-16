import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

// lines read into here to be parsed
public class InstructionObject {
	String instructionType;
	String subjectName;
	String objectName;
	int val;
	boolean badCommand;
	public InstructionObject(){
		badCommand = false;
	}
	public void checkCommand(String command) {
		command = command.toLowerCase();
		Scanner scan = new Scanner(command);
		String first = scan.next();
		instructionType = first;
		if (first.equals("write")){
			if (!checkWrite(scan))
				instructionType = "bad";
		}
		else if (first.equals("read")){
			if (!checkRead(scan))
				instructionType = "bad";
		}
		else {
			// bad command
			instructionType = "bad";
		}
	}
	
	public boolean checkWrite(Scanner scan){
		subjectName = checkAndMove(scan);
		objectName = checkAndMove(scan);
		if (scan.hasNextInt()){
			val = scan.nextInt();
		}
		else {
			instructionType = "bad";
		}
		return !scan.hasNext();
	}
	
	public boolean checkRead (Scanner scan){
		subjectName = checkAndMove(scan);
		objectName = checkAndMove(scan);
		return !scan.hasNext();
	}
	
	public String checkAndMove (Scanner scan){
		if (scan.hasNext()){
			return scan.next();
		}
		instructionType = "bad";
		return "";
	}
}
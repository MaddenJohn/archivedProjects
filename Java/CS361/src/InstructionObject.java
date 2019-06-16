import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

// lines read into here to be parsed
public class InstructionObject {
	String instructionType;
	String subjectName;
	String objectName;
	public InstructionObject(){

	}
	public void checkCommand(String command) {
		command = command.toLowerCase();
		Scanner scan = new Scanner(command);
		String first = scan.next();
		if (first.equals("write")){
			if (checkWrite(scan))
				System.out.println(command);
			else
				System.out.println(BadInstruction.BadInstruction);
		}
		else if (first.equals("read")){
			if (checkRead(scan))
				System.out.println(command);
			else
				System.out.println(BadInstruction.BadInstruction);
		}
		else {
			// bad command
			System.out.println(BadInstruction.BadInstruction);
		}
	}
	
	public boolean checkWrite(Scanner scan){
		return checkAndMove(scan) && checkAndMove(scan) && checkAndMove(scan);
	}
	
	public boolean checkRead (Scanner scan){
		
		return checkAndMove(scan) && checkAndMove(scan);
	}
	
	public boolean checkAndMove (Scanner scan){
		if (scan.hasNext()){
			scan.next();
			return true;
		}
		return false;
	}
}
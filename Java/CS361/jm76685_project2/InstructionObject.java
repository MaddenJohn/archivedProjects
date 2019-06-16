import java.util.Scanner;
/*
 * This class is used to help parse the instructions passed in and store them into fields to be
 * used when executing these instructions easily. 
 */
public class InstructionObject {
	String instructionType;
	String subjectName;
	String objectName;
	int val;
	boolean badCommand;
	// This initialization keeps many of the fields null for checking purposes later. 
	public InstructionObject(){
		badCommand = false;
	}
	
	public void setParse(String instr, String sub, String obj, int val){
		instructionType = instr;
		subjectName = sub;
		objectName = obj;
		this.val = val;
	}
	
	/*
	 * This method is the main parsing method. For instructions that have more or less arguments
	 * based on the type, or invalid instructions, this method will be able to find them and set the
	 * type to BAD if this is the case. If there are the correct amount of arguments based on the type 
	 * then the function will set the type appropriately, as well as setting the appropriate fields
	 * based on this type.
	 */
	public void checkCommand(String command) {
		command = command.toLowerCase();
		Scanner scan = new Scanner(command);
		String first = "";
		if (scan.hasNext())
			first = scan.next();
		else 
			first = instructionType = "bad";
		instructionType = first;
		if (first.equals("write")){
			if (!checkWrite(scan))
				instructionType = "bad";
		}
		else if (first.equals("read")){
			if (!checkRead(scan))
				instructionType = "bad";
		}
		else if (first.equals("create")){
			if (!checkCreate(scan))
				instructionType = "bad";
		}
		else if (first.equals("destroy")){
			if (!checkDestroy(scan))
				instructionType = "bad";
		}
		else if (first.equals("run")){
			if (!checkRun(scan))
				instructionType = "bad";
		}
		else {
			instructionType = "bad";
		}
	}
	
	// This function is tailored to check the arguments of a write command to  make sure it has 
	// the correct amount of arguments and a integer for the last argument.
	// This method returns false if there are too many arguments.
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
	
	// This function is tailored to check the arguments of a read command to  make sure it has 
	// the correct amount of arguments. This method returns false if there are too many arguments.
	public boolean checkRead (Scanner scan){
		subjectName = checkAndMove(scan);
		objectName = checkAndMove(scan);
		return !scan.hasNext();
	}
	
	// This function simple checks for the next token and returns this token. If a token is not found 
	// it set the type to BAD, and any subsequent call will not overwrite this. 
	public String checkAndMove (Scanner scan){
		if (scan.hasNext()){
			return scan.next();
		}
		instructionType = "bad";
		return "";
	}
	
	// Checks the create command
	public boolean checkCreate (Scanner scan){
		subjectName = checkAndMove(scan);
		objectName = checkAndMove(scan);
		return !scan.hasNext();
	}
	
	// Checks the destroy command and sets the appropriate variables
	public boolean checkDestroy (Scanner scan){
		subjectName = checkAndMove(scan);
		objectName = checkAndMove(scan);
		return !scan.hasNext();
	}
	
	// Checks the run command and sets the appropriate variables
	public boolean checkRun (Scanner scan){
		subjectName = checkAndMove(scan);
		return !scan.hasNext();
	}
	
	// Prints the parse Object information for debugging
	public void printParse (){
		System.out.println("" + instructionType + subjectName + objectName + val);
	}
}
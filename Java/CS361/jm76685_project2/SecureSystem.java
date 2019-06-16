import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
/*
 *  The top-level class (SecureSystem) manages subjects and the reference monitor,
 *  and also serves as the command interpreter. It reads successive instructions
 *  from the instruction list, parses them, and submits them to the reference 
 *  monitor, which asks the ObjectManager to perform them (or not). 
 *    
 *  The value returned by the reference monitor is passed to the subject 
 *  executing the instruction.
 */
public class SecureSystem {
	private static ReferenceMonitor referenceMonitor;
	private static ArrayList<Subject> subjectList;
	// Initializes the SecureSystem. This will help in accessing the reference monitor and printing the state
	public SecureSystem (){
		referenceMonitor = new ReferenceMonitor();
		subjectList = new ArrayList<Subject>();
	}
	
	// Creates a new subject and adds this to the subjectList
	public void createSubject (String name, int lvl){
		subjectList.add(new Subject(name.toLowerCase(), lvl));
	}
	
	public void createSubject (String name, int lvl, ByteArrayOutputStream output){
		subjectList.add(new Subject(name.toLowerCase(), lvl, output));
	}
	
	// returns the reference monitor
	public static ReferenceMonitor getReferenceMonitor(){
		return referenceMonitor;
	}
	
	public ArrayList<Subject> getSubjectList(){
		return subjectList;
	}
	
	// Main method, which does the intializing, and reads the data from the file. Also makes the appropriate
	// calls for parsing this data and eventually executing the actions. Finalls calls the printState()
	public static void main(String[] args) {
		SecureSystem sys = new SecureSystem();
		int low  = SecurityLevel.LOW;
		int high = SecurityLevel.HIGH;

		sys.createSubject("lyle", low);
		sys.createSubject("hal", high);
		sys.getReferenceMonitor().createNewObject("Lobj", low);
		sys.getReferenceMonitor().createNewObject("Hobj", high);
		
		String fileName = "";
		if (args.length > 0)
			fileName = args[0];
		File file = new File(fileName);
		System.out.println("Reading from file: " + fileName + "\n");
		
		InstructionObject parse = new InstructionObject();
		Scanner scan;
		try {
			scan = new Scanner(file);
			while (scan.hasNextLine()){
				String command = scan.nextLine().toLowerCase();
				parse.checkCommand(command);
				referenceMonitor.doAction(parse, subjectList);
				printState();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
	}

	// Prints all the information found in the subjects and objects
	public static void printState (){
		System.out.println("The current state is: ");
		for (Object element : getReferenceMonitor().objectList){
			String temp = "\t" + element.getName() + " has value: " + element.getVal();
			System.out.println(temp);
		}
		for (Subject element : subjectList){
			String temp = "\t" + element.getName() + " has recently read: " + element.getVal();
			System.out.println(temp);
		}
		System.out.println();
	}

}











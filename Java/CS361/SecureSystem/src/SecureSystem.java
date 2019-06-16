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
	public SecureSystem (){
		referenceMonitor = new ReferenceMonitor();
		subjectList = new ArrayList<Subject>();
	}
	
	public void createSubject (String name, int lvl){
		subjectList.add(new Subject(name.toLowerCase(), lvl));
	}
	
	public ReferenceMonitor getReferenceMonitor(){
		return this.referenceMonitor;
	}
	
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
				printState(sys);
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
	}

	public static void printState (SecureSystem sys){
		System.out.println("The current state is: ");
		for (Object element : sys.getReferenceMonitor().objectList){
			String temp = "\t" + element.getName() + " has value: " + element.getVal();
			System.out.println(temp);
		}
		for (Subject element : sys.subjectList){
			String temp = "\t" + element.getName() + " has recently read: " + element.getVal();
			System.out.println(temp);
		}
		System.out.println();
	}

}











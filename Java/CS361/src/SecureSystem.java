import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class SecureSystem {
	
	public SecureSystem (){
		
	}
	
	public static void main(String[] args) {
		String fileName = "";
		if (args.length > 0)
			fileName = args[0];
		File file = new File(fileName);
		
		InstructionObject parse = new InstructionObject();
		Scanner scan;
		try {
			scan = new Scanner(file);
			while (scan.hasNextLine()){
				String command = scan.nextLine();
				parse.checkCommand(command);
				printState();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		
		/*
		SecurityLevel low = SecurityLevel.LOW;
		SecurityLevel high = SecurityLevel.HIGH;
		Subject lyle = new Subject ("lyle", low);
		Subject hal = new Subject ("hal", high);
		Object lobj = new Object (0, "lobj", low);
		Object hobj = new Object (0, "hobj", high);
		
		// Example Code
		SecurityLevel low  = SecurityLevel.LOW;
		SecurityLevel high = SecurityLevel.HIGH;

		sys.createSubject("lyle", low);
		sys.createSubject("hal", high);
		sys.getReferenceMonitor().createNewObject("Lobj", low);
		sys.getReferenceMonitor().createNewObject("Hobj", high);*/
		
	}

	public static void printState (){
		//System.out.println("State: ");
	}

}











import java.util.ArrayList;

// maintains labels, prevent any changes to labels
// checks BLP properties, if legal tells ObjectManager to perform
// always returns an integer value to the subject: the value of the 
// object read, if the command was a legal READ; and 0 otherwise
public class ReferenceMonitor {
	ArrayList<Object> objectList;
	ObjectManager objMan;
	boolean isVerbose;
	// initiallizes the reference monitor
	public ReferenceMonitor (){
		objectList = new ArrayList<Object>();
		objMan = new ObjectManager();
		isVerbose = false;
	}
	
	// Creates a new object and stores it on the object List
	public void createNewObject(String name, int lvl){
		objectList.add(new Object(name.toLowerCase(), lvl, 0));
	}
	
	// Sets the verbose variable if there is a need to print
	public void setVerbose(boolean verbose){
		isVerbose = verbose;
	}
	
	// Gets the object based on the name
	public Object getObject(ArrayList<Object> list, String name){
		for (Object element: list){
			if (element.getName().toLowerCase().equals(name))
				return element;
		}
		return null;
	}
	
	// Gets the subject based on the name
	public Subject getSubject(ArrayList<Subject> list, String name){
		for (Subject element: list){
			if (element.getName().toLowerCase().equals(name))
				return element;
		}
		return null;
	}

	// Determines which action to take based on the information passed and prints BadInstruction if there is
	// bad input. 
	public void doAction(InstructionObject parse, ArrayList<Subject> subjectList) {
		String type = parse.instructionType;
		String subjectName = parse.subjectName;
		String objectName = parse.objectName;
		int val = parse.val;
		Subject sub = getSubject(subjectList, subjectName);
		Object obj = getObject(objectList, objectName);
		String result = "";
		
		if (type.equals("write") && sub != null && obj != null){
			result = executeWrite(subjectName, objectName, obj, sub, val);
		}
		else if (type.equals("read")&& sub != null && obj != null){
			result = executeRead(subjectName, objectName, obj, sub);
		}
		else if (type.equals("create") && sub != null){
			result = executeCreate(subjectName, objectName, obj, sub);
		}
		else if (type.equals("destroy") && sub != null && obj != null){
			result = executeDestroy(subjectName, objectName, obj, sub);
		}
		else if (type.equals("run") && sub != null){
			result = executeRun(subjectName, sub);
		}
		else {
			result = BadInstruction.BadInstruction;
		}
		if (isVerbose){
			System.out.println(result);
		}
	}
	
	// Reads as long as the Bell and LaPadula rules are followed, using the Object Manager
	public String executeRead(String subjectName, String objectName, Object obj, Subject sub){
		String result = subjectName + " reads " + objectName;
		if (sub.getLabel() >= obj.getLabel())
			sub.setVal(objMan.readVal(obj));
		else
			sub.setVal(0);
		return result;
	}
	
	// Writes as long as the Bell and LaPadula rules are followed, using the Object Manager
	public String executeWrite(String subjectName, String objectName, Object obj, Subject sub, int val){
		String result = subjectName + " writes value " + val + " to "+ objectName;
		if (sub.getLabel() <= obj.getLabel())
			objMan.writeVal(val, obj);
		return result;
	}
	
	// Creates a new object, setting its label to the subject
	public String executeCreate(String subjectName, String objectName, Object obj, Subject sub){
		String result = subjectName + " created " + objectName;
		if(obj == null){
			createNewObject(objectName, sub.getLabel());
			return result;
		}
		return result;
	}
	
	// Destroys the object if it is there and the subjects label is <= the object Label
	public String executeDestroy(String subjectName, String objectName, Object obj, Subject sub){
		String result = subjectName + " destroyed " + objectName;
		if(sub.getLabel() <= obj.getLabel() && obj != null){
			objectList.remove(obj);
		}
		return result;
	}
	
	// Runs the specified subject's command, which is only done for the lower level subject, takes a bit, adds it
	// to current string of bits, and if this current string = size 8, then write to output stream. This is the 
	// main part to the covert operation which is only used on the lower level subject. 
	public String executeRun(String subjectName, Subject sub){
		if (subjectName.equals("lyle")){
			String covertString = sub.getCovertString();
			if (covertString.length() < 8){
				sub.setCovertString(covertString + sub.getVal());
			}
			else {
				byte temp = Byte.parseByte(covertString, 2);
				sub.getOutput().write(temp);
				sub.setCovertString("" + sub.getVal());
			}
		}
		String result = "run " + subjectName;
		return result;
	}
	
}
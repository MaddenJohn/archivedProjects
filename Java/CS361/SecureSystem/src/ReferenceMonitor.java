import java.util.ArrayList;

// maintains labels, prevent any changes to labels
// checks BLP properties, if legal tells ObjectManager to perform
// always returns an integer value to the subject: the value of the 
// object read, if the command was a legal READ; and 0 otherwise
public class ReferenceMonitor {
	ArrayList<Object> objectList;
	public ReferenceMonitor (){
		objectList = new ArrayList<Object>();
	}
	
	public void createNewObject(String name, int lvl){
		objectList.add(new Object(name.toLowerCase(), lvl, 0));
	}
	
	public Object getObject(ArrayList<Object> list, String name){
		for (Object element: list){
			if (element.getName().toLowerCase().equals(name))
				return element;
		}
		return null;
	}
	
	public Subject getSubject(ArrayList<Subject> list, String name){
		for (Subject element: list){
			if (element.getName().toLowerCase().equals(name))
				return element;
		}
		return null;
	}

	public void doAction(InstructionObject parse, ArrayList<Subject> subjectList) {
		if (parse.instructionType.equals("bad"))
			System.out.println(BadInstruction.BadInstruction);
		else {
			String result = "";
			String type = parse.instructionType;
			String subjectName = parse.subjectName;
			String objectName = parse.objectName;
			int val = parse.val;
			Subject sub = getSubject(subjectList, subjectName);
			Object obj = getObject(objectList, objectName);
			if (type.equals("write")){
				System.out.println(executeWrite(subjectName, objectName, obj, sub, val));
			}
			else {
				System.out.println(executeRead(subjectName, objectName, obj, sub));
			}
			
		}
	}
	
	public String executeRead(String subjectName, String objectName, Object obj, Subject sub){
		String result = result = subjectName + " reads " + objectName;
		if (sub.label >= obj.label)
			sub.setVal(obj.val);
		else
			sub.setVal(0);
		return result;
	}
	
	public String executeWrite(String subjectName, String objectName, Object obj, Subject sub, int val){
		String result = subjectName + " writes value " + val + " to "+ objectName;
		if (sub.label <= obj.label)
			obj.setVal(val);
		return result;
	}
}
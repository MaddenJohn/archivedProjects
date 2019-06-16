// objects modified through this manager
public class ObjectManager {

	// Modifies the val stored in object to val
	public void writeVal(int val, Object obj) {
		obj.setVal(val);
	}
	
	// returns the value stored in the object
	public int readVal(Object obj) {
		return obj.getVal();
	}

}

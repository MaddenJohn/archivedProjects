public class Object {
	int val;
	String name;
	SecurityLevel label;
	public Object (int val, String n, SecurityLevel label){
		this.val = val;
		name = n;
		this.label = label;
	}

	public void setVal (int newVal){
		val = newVal;
	}

	public int getVal (){
		return val;
	}
}
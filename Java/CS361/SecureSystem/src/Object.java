public class Object {
	int val;
	String name;
	int label;
	public Object (String n, int label, int val){
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
	
	public String getName(){
		return name;
	}
}
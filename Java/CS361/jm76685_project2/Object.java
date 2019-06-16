/*
 * Object class used for each object in this project. Basic methods to update and get these values are here
 * Since these values will not be accessible outside the method. 
 */
public class Object {
	private int val;
	private String name;
	private int label;
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
	
	public int getLabel(){
		return label;
	}
}
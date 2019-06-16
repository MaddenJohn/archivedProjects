public class Subject {
	String name;
	int TEMP;
	int label;
	public Subject (String n, int label){
		name = n;
		TEMP = 0;
		this.label = label;
	}

	public void setVal (int newVal){
		TEMP = newVal;
	}

	public int getVal() {
		return TEMP;
	}
	
	public String getName() {
		return name;
	}
}
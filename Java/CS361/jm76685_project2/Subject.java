import java.io.ByteArrayOutputStream;

/*
 * Subject class used for each object in this project. Basic methods to update and get these values are here
 * Since these values will not be accessible outside the method. 
 */
public class Subject {
	private String name;
	private int TEMP;
	private int label;
	private String covertString;
	private ByteArrayOutputStream output;
	public Subject (String n, int label){
		name = n;
		TEMP = 0;
		this.label = label;
		covertString = "";
		this.output = null;
	}
	
	public Subject (String n, int label, ByteArrayOutputStream output){
		name = n;
		TEMP = 0;
		this.label = label;
		covertString = "";
		this.output = output;
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
	
	public int getLabel(){
		return label;
	}
	
	public String getCovertString (){
		return covertString;
	}
	
	public void setCovertString (String s){
		covertString = s;
	}
	
	public ByteArrayOutputStream getOutput (){
		return output;
	}
	
	
}
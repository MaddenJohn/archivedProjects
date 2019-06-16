/*
 * Object to hold the user data.
 */
public class User {
	public String fName;
	public String lName;
	public String encryption;
	public String name;
	public User(String firstName, String lastName, String enc){
		fName = firstName;
		lName = lastName;
		name = firstName + " " + lastName;
		encryption = enc;
	}
	
	public User(String name, String enc){
		this.name = name;
		encryption = enc;
	}
}

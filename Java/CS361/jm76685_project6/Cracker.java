import java.util.ArrayList;
/*
 * Class to be used to use threads. Calls PasswordCrack for actual functionality in the run() function
 */
public class Cracker implements Runnable{
	ArrayList<User> users;
	ArrayList<String> dictionary;
	int id;
	public Cracker(ArrayList<User> user, ArrayList<String> dict, int id){
		this.users = user;
		dictionary = dict;
		this.id = id;
	}

	public void run() {
		double start = System.currentTimeMillis();
		for (User u: users){
			String password = PasswordCrack.getPassword(u.encryption, dictionary);
			if (password != null)
				System.out.println("The password for user " + u.name + " is " + password);
			
		}	
		// print last threads, which are usually longest, for timing
		//if (id > 0)
		//	System.out.println("Seconds passed: " + ((System.currentTimeMillis() - start) / 1000));
	}
}

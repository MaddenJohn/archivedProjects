import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

/*
 * 
 * executed by java PasswordCrack inputFile1 inputFile2 where inputFile1 is the dictionary
 * and inputFile2 is a list of passwords to crack.
 */
public class PasswordCrack {

	/*
	 * Main Method which handles parting and creation of the dictionaries to be
	 * used Also calls the build threads function, which does all of the actual
	 * testing for the passwords.
	 */
	public static void main(String[] args) throws IOException {
		String dictionaryFile = "";
		String passwordList = "";
		// Parse the command line arguments
		if (args.length == 2) {
			dictionaryFile = args[0];
			passwordList = args[1];
		} else {
			System.err.println("Error in number of arguments");
			System.exit(1);
		}

		File dFile = new File(dictionaryFile);
		File passFile = new File(passwordList);
		FileReader fileReader = new FileReader(dFile);
		BufferedReader dictBR = new BufferedReader(fileReader);
		FileReader keyReader = new FileReader(passFile);
		BufferedReader passBR = new BufferedReader(keyReader);
		ArrayList<String> dictionary = new ArrayList<String>();
		// creation of the dictionaries to be used
		String word = dictBR.readLine();
		int i = 0;
		while (word != null) {
			dictionary.add(word);
			word = dictBR.readLine();
		}

		for (String w : commonPasswords) {
			commonDict.add(w);
		}

		String userInfo = passBR.readLine();
		ArrayList<User> users = new ArrayList<User>();
		// Adds user objects into an arrayList so that we can check them
		// individually later
		while (userInfo != null) {
			Scanner s = new Scanner(userInfo);
			s.useDelimiter(":");
			s.next();
			String encryption = s.next();
			s.next();
			s.next();
			String name = s.next();

			Scanner s2 = new Scanner(name);
			String firstName = s2.next();
			String lastName = s2.next();
			// adds all names to a smaller dictionary for faster checking
			commonDict.add(firstName);
			commonDict.add(lastName);
			s2.close();
			users.add(new User(firstName, lastName, encryption));
			userInfo = passBR.readLine();
			s.close();
		}
		dictBR.close();
		passBR.close();
		buildThreads(dictionary, users.size(), users);

	}

	/*
	 * Threads function, which creates a number of threads to run thruogh
	 * checking each user separately to speed up the process.
	 */
	private static void buildThreads(ArrayList<String> dictionary, int size, ArrayList<User> users) {
		ArrayList<ArrayList<User>> usersList = new ArrayList<ArrayList<User>>();
		for (int j = 0; j < size; j++) {
			usersList.add(new ArrayList<User>());
		}
		int j = 0;
		for (User u : users) {
			usersList.get(j).add(u);
			j = (j + 1) % size;
		}
		for (int k = 0; k < size; k++) {
			Thread t = new Thread(new Cracker(usersList.get(k), dictionary, k));
			t.start();
		}
	}

	// 2016 most common passwords
	static String[] commonPasswords = { "123456789", "qwerty", "12345678", "111111", "1234567890", "1234567",
			"password", "123123", "987654321", "qwertyuiop", "mynoob", "123321", "666666", "18atcskd2w", "7777777",
			"1q2w3e4r", "654321", "555555", "3rjs1la7qe", "google", "1q2w3e4r5t", "123qwe", "zxcvbnm", "1q2w3e" };

	static ArrayList<String> commonDict = new ArrayList<String>();

	/*
	 * Main function to actually find the password for the user. Returns the
	 * string value or null if not found in the dictionary. This
	 * function is optimized to check for the easiest methods first of finding
	 * the encryption before moving to a harder method such as a second mangle.
	 */
	public static String getPassword(String encryption, ArrayList<String> dict) {
		String salt = encryption.substring(0, 2);
		for (String word : commonDict) {
			String result = checkword(salt, word, encryption);
			if (result != null)
				return result;

		}

		for (String word : commonDict) {
			String result = secondSimpleCheck(salt, word, encryption, true);
			if (result != null)
				return result;

		}

		for (String word : dict) {
			String result = simpleCheck(salt, word, encryption, false);
			if (result != null)
				return result;
		}
		for (String word : dict) {
			String result = complexCheck(salt, word, encryption);
			if (result != null)
				return result;
		}
		for (String word : dict) {
			String result = secondSimpleCheck(salt, word, encryption, true);
			if (result != null)
				return result;
		}
		return null;
		//return "Not Found ***";
	}

	// utility function to check a word entirely throug hthe dictionary
	private static String checkword(String salt, String word, String encryption) {
		String result = simpleCheck(salt, word, encryption, true);
		if (result != null)
			return result;
		result = complexCheck(salt, word, encryption);
		if (result != null)
			return result;
		return null;
	}

	/*
	 * prepend a character to the string, e.g., @string; append a character to
	 * the string, e.g., string9;
	 */
	private static String lessComplexCheck(String salt, String word, String encryption) {
		// prepend/append num
		for (int i = 48; i < 58; i++) {
			if (jcrypt.crypt(salt, (char) i + word).equals(encryption))
				return (char) i + word;
			if (jcrypt.crypt(salt, word + (char) i).equals(encryption))
				return word + (char) i;
		}
		return null;
	}

	/*
	 * prepend a character to the string, e.g., @string; append a character to
	 * the string, e.g., string9;
	 */
	private static String complexCheck(String salt, String word, String encryption) {
		// prepend/append
		for (int i = 32; i < 127; i++) {
			if (i < 48 || i >= 58) {
				if (jcrypt.crypt(salt, (char) i + word).equals(encryption))
					return (char) i + word;
				if (jcrypt.crypt(salt, word + (char) i).equals(encryption))
					return word + (char) i;
			}
		}
		return null;
	}

	/*
	 * Runs through the following checks for a specific word to see if it
	 * matches the encryption: delete the first character from the string, e.g.,
	 * tring; delete the last character from the string, e.g., strin; reverse
	 * the string, e.g., gnirts; duplicate the string, e.g., stringstring;
	 * reflect the string, e.g., stringgnirts or gnirtsstring; uppercase the
	 * string, e.g., STRING; lowercase the string, e.g., string; capitalize the
	 * string, e.g., String; ncapitalize the string, e.g., sTRING; toggle case
	 * of the string, e.g., StRiNg or sTrInG;
	 */
	private static String simpleCheck(String salt, String word, String encryption, Boolean lessCheck) {
		// check exact string
		if (jcrypt.crypt(salt, word).equals(encryption))
			return word;
		// delete first char
		if (jcrypt.crypt(salt, word.substring(1)).equals(encryption))
			return word.substring(1);

		// delete last char
		if (jcrypt.crypt(salt, word.substring(0, word.length() - 1)).equals(encryption))
			return word.substring(0, word.length() - 1);

		String revWord = new StringBuffer(word).reverse().toString();
		// reverse word
		if (jcrypt.crypt(salt, revWord).equals(encryption))
			return revWord;

		// duplicate word
		if (jcrypt.crypt(salt, word + word).equals(encryption))
			return word + word;

		// reflect word
		if (jcrypt.crypt(salt, revWord + word).equals(encryption))
			return revWord + word;

		// reflect word
		if (jcrypt.crypt(salt, word + revWord).equals(encryption))
			return word + revWord;

		// lowercase
		if (jcrypt.crypt(salt, word.toLowerCase()).equals(encryption))
			return word.toLowerCase();

		// uppercase
		if (jcrypt.crypt(salt, word.toUpperCase()).equals(encryption))
			return word.toUpperCase();

		// capitalize string
		if (jcrypt.crypt(salt, word.substring(0, 1).toUpperCase() + word.substring(1)).equals(encryption))
			return word.substring(0, 1).toUpperCase() + word.substring(1);

		// ncapitalize
		if (jcrypt.crypt(salt, word.substring(0, 1).toLowerCase() + word.substring(1).toUpperCase()).equals(encryption))
			return word.substring(0, 1).toLowerCase() + word.substring(1).toUpperCase();

		// toggle case
		StringBuilder toggle1 = new StringBuilder();
		StringBuilder toggle2 = new StringBuilder();
		int index = 0;
		for (char c : word.toCharArray()) {
			if (index % 2 == 0)
				toggle1.append(Character.toLowerCase(c));
			else
				toggle1.append(Character.toUpperCase(c));
			if (index % 2 == 1)
				toggle2.append(Character.toLowerCase(c));
			else
				toggle2.append(Character.toUpperCase(c));
			index++;
		}
		if (jcrypt.crypt(salt, toggle1.toString()).equals(encryption))
			return toggle1.toString();
		if (jcrypt.crypt(salt, toggle2.toString()).equals(encryption))
			return toggle2.toString();

		// prepend/append num
		if (lessCheck) {
			String result = lessComplexCheck(salt, word, encryption);
			return result;
		}
		for (int i = 48; i < 58; i++) {
			if (jcrypt.crypt(salt, (char) i + word).equals(encryption))
				return (char) i + word;
			if (jcrypt.crypt(salt, word + (char) i).equals(encryption))
				return word + (char) i;
		}
		return null;
	}

	// Utility function to mangle the word a second time
	private static String secondSimpleCheck(String salt, String word, String encryption, boolean check) {
		// delete first char
		if (check) {
			String result = simpleCheck(salt, word.substring(1), encryption, false);
			if (result != null)
				return result;
		}

		// delete last char
		if (check) {
			String result = simpleCheck(salt, word.substring(0, word.length() - 1), encryption, false);
			if (result != null)
				return result;
		}

		String revWord = new StringBuffer(word).reverse().toString();
		// reverse word
		if (check) {
			String result = simpleCheck(salt, revWord, encryption, false);
			if (result != null)
				return result;
		}

		// dup word
		if (check) {
			String result = simpleCheck(salt, word + word, encryption, false);
			if (result != null)
				return result;
		}

		// reflect
		if (check) {
			String result = simpleCheck(salt, revWord + word, encryption, false);
			if (result != null)
				return result;
		}
		// reflect
		if (check) {
			String result = simpleCheck(salt, word + revWord, encryption, false);
			if (result != null)
				return result;
		}

		// lowercase
		if (check) {
			String result = simpleCheck(salt, word.toLowerCase(), encryption, false);
			if (result != null)
				return result;
		}

		// uppercase
		if (check) {
			String result = simpleCheck(salt, word.toUpperCase(), encryption, false);
			if (result != null)
				return result;
		}

		// capitalize string
		if (check) {
			String result = simpleCheck(salt, word.substring(0, 1).toUpperCase() + word.substring(1), encryption,
					false);
			if (result != null)
				return result;
		}

		// ncapitalize
		if (check) {
			String result = simpleCheck(salt, word.substring(0, 1).toLowerCase() + word.substring(1).toUpperCase(),
					encryption, false);
			if (result != null)
				return result;
		}

		// toggle case
		StringBuilder toggle1 = new StringBuilder();
		StringBuilder toggle2 = new StringBuilder();
		int index = 0;
		for (char c : word.toCharArray()) {
			if (index % 2 == 0)
				toggle1.append(Character.toLowerCase(c));
			else
				toggle1.append(Character.toUpperCase(c));
			if (index % 2 == 1)
				toggle2.append(Character.toLowerCase(c));
			else
				toggle2.append(Character.toUpperCase(c));
			index++;
		}
		if (check) {
			String result = simpleCheck(salt, toggle1.toString(), encryption, false);
			if (result != null)
				return result;
		}

		if (check) {
			String result = simpleCheck(salt, toggle2.toString(), encryption, false);
			if (result != null)
				return result;
		}
		return null;
	}
}

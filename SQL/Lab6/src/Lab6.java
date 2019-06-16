// 2564 total seconds to run
// (2,164)
import java.sql.*;
import java.util.LinkedList;

public class Lab6 {
	public static String USERNAME = new String("system");
	public static String PASSWORD = new String("kleenex");

	public static void main(String[] args) throws ClassNotFoundException {

		// Load the Oracle Driver
		try {
			Class.forName("oracle.jdbc.driver.OracleDriver");
		} catch (ClassNotFoundException e) {
			System.out.println("whaa");
		}

		try {
			// Get a connection from the connection factory
			Connection con = DriverManager.getConnection("jdbc:oracle:thin://localHost:5500/em/shell", USERNAME,
					PASSWORD);

			// Show some database/driver metadata
			SQLUtil.printDriverInfo(con);

			// Create a Statement object so we can submit SQL statements to the
			// driver
			Statement stmt = con.createStatement();

			// Submit the statement
			LinkedList<Integer> queue = new LinkedList<Integer>();
			for (int i = 0; i < 3000000; i++)
				queue.add(i);
			
			long startTime = System.currentTimeMillis();
			long lastTime = startTime;
			for (int i = 0; i < 3000000; i++) {
				boolean print = i % 50000 == 0;
				String insertRow = "insert into benchmark2 values (" + queue.removeFirst() + "," + randomNum(50000) + ","
						+ randomNum(50000) + ",\'" + randomString(10) + "\')";
				if (print)
					System.out.print(insertRow + "  Sorted  ...");
				int rowsAffected = stmt.executeUpdate(insertRow);
				if (rowsAffected == 1 && print) {
					System.out.print("OK, i value: " + i);
					long runTime = System.currentTimeMillis();
					System.out.println("    seconds to run: " + (runTime - startTime) / 1000 + " interval: "
							+ (runTime - lastTime) / 1000);
					lastTime = runTime;
				}

			}
			long endTime = System.currentTimeMillis();

			System.out.println("total seconds to run: " + (endTime - startTime) / 1000);

			// Close the statement
			stmt.close();

			// Close the connection
			con.close();
		} catch (SQLException e) {
			SQLUtil.printSQLExceptions(e);
		}
	}

	static String randomNum(int range) {
		String result = "";
		result += (int) (Math.random() * range);
		return result;
	}

	static String randomString(int range) {
		String result = "";
		for (int i = 0; i < range; i++) {
			int letter = (int) (Math.random() * 26);
			result += (char) ('z' - letter);
		}
		return result;
	}
}
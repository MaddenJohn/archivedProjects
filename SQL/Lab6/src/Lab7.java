import java.sql.*;

public class Lab7 {
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
			
			long startTime = System.currentTimeMillis();
			for(int i = 20000; i< 30000; i += 1000){ 
				// ResultSet is returned from execute query, which can be used in display data method
				for(int j = 0; j < 10; j++){
					stmt.executeQuery("SELECT * FROM benchmark WHERE ColumnA = " + i);
					//stmt.executeQuery("SELECT * FROM benchmarkU WHERE ColumnA = " + i + " AND ColumnB = " + i);
				}
				System.out.println("Done with: " + i);
			}
			long endTime = System.currentTimeMillis();
			long secondsTime = (endTime - startTime) / 1000;
			System.out.println("total seconds to run: " + secondsTime + "   avg: " + secondsTime / 100);

			// Close the statement
			stmt.close();

			// Close the connection
			con.close();
		} catch (SQLException e) {
			SQLUtil.printSQLExceptions(e);
		}
	}

	static void displayData(ResultSet rs){
		try{
			while ( rs.next() ) {
				int columnA = rs.getInt("columnA");
			    int columnB = rs.getInt("columnB");
			    int key = rs.getInt("theKey");
			    String filler = rs.getString("filler");
			    System.out.println("PrimaryKey: " + key + " column A: " + columnA + "  column B " + columnB + " filler: " + filler);
				}
			}
		catch (SQLException e) {
			SQLUtil.printSQLExceptions(e);
		}
	}
}
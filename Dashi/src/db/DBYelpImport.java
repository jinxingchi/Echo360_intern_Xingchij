
package db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Create DB tables in MySQL.
 * how to convert data from yelp json to database
 *
 */
public class DBYelpImport {

    public static void main(String[] args) {// not part of server
   	 try {
         // Ensure the driver is imported.
   		 Class.forName("com.mysql.jdbc.Driver").newInstance();// initialization JDBC instance
   		 Connection conn = null;

   		 try {
   			 System.out.println("Connecting to \n" + DBUtil.URL);
   			 //DriverManager is static, which can be used after dot
   			 conn = DriverManager.getConnection(DBUtil.URL);
   		 } catch (SQLException e) {
   			 //if error, print errors
   			 System.out.println("SQLException " + e.getMessage());
   			 System.out.println("SQLState " + e.getSQLState());
   			 System.out.println("VendorError " + e.getErrorCode());
   		 }
   		 if (conn == null) {// if connection is not successful
   			 return;
   		 }
   		 // Step 1 Drop tables in case they exist.
   		 Statement stmt = conn.createStatement();//statement is 每次sql的指令
   		 //顺序不能换
   		 String sql = "DROP TABLE IF EXISTS history";
   		 stmt.executeUpdate(sql);
   		 
   		 sql = "DROP TABLE IF EXISTS restaurants";
   		 stmt.executeUpdate(sql);

   		 sql = "DROP TABLE IF EXISTS users";
   		 stmt.executeUpdate(sql);
   		 
   		 // ------------------------------- //
   		 //顺序不能换
   		 
   		 sql = "CREATE TABLE restaurants "
   				 + "(business_id VARCHAR(255) NOT NULL, "
   				 + " name VARCHAR(255), " + "categories VARCHAR(255), "
   				 + "city VARCHAR(255), " + "state VARCHAR(255), "
   				 + "stars FLOAT," + "full_address VARCHAR(255), "
   				 + "latitude FLOAT, " + " longitude FLOAT, "
   				 + "image_url VARCHAR(255),"
   				 + "url VARCHAR(255),"
   				 + " PRIMARY KEY ( business_id ))";
   		 stmt.executeUpdate(sql);

   		 sql = "CREATE TABLE users "
   				 + "(user_id VARCHAR(255) NOT NULL, "
   				 + " password VARCHAR(255) NOT NULL, "
   				 + " first_name VARCHAR(255), last_name VARCHAR(255), "
   				 + " PRIMARY KEY ( user_id ))";
   		 stmt.executeUpdate(sql);
   		 
   		 // automatically create PK.
   		 // business_id in this table, point to "business_id" in the restaurants table
   		 // business_id in this table must also exist in the restaurant table
   		 sql = "CREATE TABLE history "
   				 + "(visit_history_id bigint(20) unsigned NOT NULL AUTO_INCREMENT, "
   				 + " user_id VARCHAR(255) NOT NULL , "
   				 + " business_id VARCHAR(255) NOT NULL, "
   				 + " last_visited_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
   				 + " PRIMARY KEY (visit_history_id),"
   				 + "FOREIGN KEY (business_id) REFERENCES restaurants(business_id),"
   				 + "FOREIGN KEY (user_id) REFERENCES users(user_id))";
   		 stmt.executeUpdate(sql);
   		 // Step 3: insert data
   		 // Create a fake user
   		 sql = "INSERT INTO users " + "VALUES (\"1111\", \"3229c1097c00d497a0fd282d586be050\", \"John\", \"Smith\")";


   		 System.out.println("\nDBYelpImport executing query:\n" + sql);
   		 stmt.executeUpdate(sql);
   		 
   		 System.out.println("DBYelpImport: import is done successfully.");
   	 } catch (Exception e) {
   		 System.out.println(e.getMessage());
   	 }
    }
}

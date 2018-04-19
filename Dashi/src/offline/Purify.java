
package offline;

import java.io.BufferedReader;
import java.io.FileReader;

import org.bson.Document;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoDatabase;

import db.DBUtil;

public class Purify {
	public static void main(String[] args) {
		MongoClient mongoClient = new MongoClient();
		MongoDatabase db = mongoClient.getDatabase(DBUtil.DB_NAME);
		// The name of the file to open.
		// Windows is different : C:\\Documents\\ratings_Musical_Instruments.csv
		String fileName = "/Users/xingchijin/Downloads/ratings_Musical_Instruments.csv";

		String line = null;

		try {
			FileReader fileReader = new FileReader(fileName);//open file

			BufferedReader bufferedReader = new BufferedReader(fileReader);//use buffer read
			while ((line = bufferedReader.readLine()) != null) {
				String[] values = line.split(",");

				db.getCollection("ratings")// build a new collection "rating"
						.insertOne(
								new Document()
										.append("user", values[0])
										.append("item", values[1])
										.append("rating",
												Double.parseDouble(values[2])));

			}
			System.out.println("Import Done!");
			bufferedReader.close();
			mongoClient.close();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}

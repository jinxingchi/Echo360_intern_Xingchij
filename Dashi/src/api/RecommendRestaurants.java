package api;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import db.DBConnection;
import db.MongoDBConnection;
import db.MySQLDBConnection;

/**
 * Servlet implementation class RecommendRestaurants
 * doPost how to write???
 */
@WebServlet("/recommendation")
public class RecommendRestaurants extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public RecommendRestaurants() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
    private static DBConnection connection = new MySQLDBConnection();

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		// allow access only if session exists
				HttpSession session = request.getSession();
				if (session.getAttribute("user") == null) {
					response.setStatus(403);
					return;
				}

//		JSONArray array = new JSONArray();
//		try {
//			if (request.getParameterMap().containsKey("user_id")) {
//				String userId = request.getParameter("user_id");
//				
//				// return some fake restaurants
//				array.put(new JSONObject().put("name", "Panda Express")
//										  .put("location", "downtown")
//										  .put("country", "US")
//						);
//				array.put(new JSONObject().put("name", "Hong Kong Express")
//										  .put("location", "uptown")
//										  .put("country", "united states")
//						);
//			}
//		} catch (JSONException e) {
//			e.printStackTrace();
//		}
//		RpcParser.writeOutput(response, array);
		JSONArray array = null;
		
		if (request.getParameterMap().containsKey("user_id")) {
			String userId = request.getParameter("user_id");
			array = connection.recommendRestaurants(userId);
		}
		RpcParser.writeOutput(response, array);


	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		// allow access only if session exists
				HttpSession session = request.getSession();
				if (session.getAttribute("user") == null) {
					response.setStatus(403);
					return;
				}

		doGet(request, response);
	}

}

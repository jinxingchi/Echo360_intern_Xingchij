//Xingchi Jin



import java.util.*;
import java.awt.*;
import java.awt.Color;
import java.awt.Graphics;

public class SpaceShip
{
	private int xPos, yPos;
	private boolean isShooting = false;
	private Color clr;
	private final int WIDTH = 40, HEIGHT = 30;
//	private final int line_x = 15, line_y = 15;


	// constructor: gen spaceship at a random place
	public  SpaceShip(){
		
		Random r = new Random();
		xPos = r.nextInt(600);	
		yPos = r.nextInt(600);	
		this.clr = Color.blue;
		isShooting = false; //shoot only when I click

	}
	//constructor: gen one spaceship at a specific position	 
	public  SpaceShip(int x, int y){

		xPos = x;
		yPos = y;
		clr = Color.blue;
		isShooting = false;
		}
	//set color to the spaceship
	public void setColor(Color c){
		clr = c;
	}
	//draw spaceships
		public void draw(Graphics g, int edge){
		//body
		g.setColor(this.clr);
		g.fillOval(xPos,yPos, WIDTH, HEIGHT);
		
		//the line
//		g.setColor(Color.blue);
//		g.drawLine(xPos-line_x, yPos, xPos, yPos+line_y);
//		g.drawLine(xPos-line_x, yPos+2*line_y, xPos, yPos+line_y);
		//the arc
		g.setColor(Color.black);
		g.drawArc(xPos+10, yPos, WIDTH, HEIGHT, 90, 180);
			
		//window 1
		g.setColor(Color.cyan);
		g.fillRect(xPos+18, yPos+5, 5, 5);
		//window2
		g.setColor(Color.cyan);
		g.fillRect(xPos+ 18, yPos+20, 5, 5);
		//window3
//		int R = (int)(Math.random()*256);
//		int G = (int)(Math.random()*256);
//		int B= (int)(Math.random()*256);
//		Color randomColor = new Color(R, G, B); //random color for the third window
//		g.setColor(randomColor);
//		g.fillRect(xPos+25, yPos+15, 4, 4);

		//laser beam
	    if (isShooting == true){
		    g.drawLine(xPos+WIDTH, yPos+HEIGHT/2, edge , yPos+HEIGHT/2);
			g.setColor(Color.blue);
	    }		
	}
	
		//set shooting
	public void setShooting(boolean b){		
		isShooting = b;
	}
	
	public String toString(){
		return " \nxPos: " + xPos + "\nyPos: "+ yPos + "\nShooting?: "  + isShooting;
		
	}//return a string
	
	//move ships
		public void move(int x, int y){
			xPos = x;
			yPos = y;
		}
		
	//methods for get position of the ship	
		
		public int getX(){
			return xPos;
		}

		public int getY(){
			return yPos;
		}
		
		public int getHeight(){
			return HEIGHT;
		}
		
		public int getWidth(){
			return WIDTH;
		}
		
		public boolean getShoot(){
			return isShooting ;
		}
		
		public Point getPosition() {
			return new Point(xPos, yPos);		//returns the position of the asteroid
		}
		
		
}





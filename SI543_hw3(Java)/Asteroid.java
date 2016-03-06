//Xingchi Jin
/*
import java.awt.Color;
import java.awt.Graphics;
import java.util.Random;

public class Asteroid {
	private int xPos, yPos;
	private Color clr;
	private  int diameter;
	private Random r = new Random();
	
	//constructor 1
	public Asteroid(){
		xPos = r.nextInt(600);
		yPos = r.nextInt(600);
		diameter = r.nextInt(50)+10;
		clr = Color.green;
	}
	
	//constructor 2
	public Asteroid(int i){
		xPos = r.nextInt(i);
		yPos = r.nextInt(i);
		diameter = r.nextInt(50)+5;
		clr = Color.green;
		
	}
	
	//set color for asteroids
	public void setColor(Color color){
		clr = color;
	}
	
	//draw asteroids
	public void draw(Graphics g){
		g.setColor(clr);
		g.fillRect(xPos, yPos, diameter, diameter);
	}
	
	//make asteroids
	public void move(int i){
		xPos = r.nextInt(i-10);
		yPos = r.nextInt(i-10);
	}
}
*/

import java.awt.Color;
import java.awt.Point;

import java.awt.Graphics;
import java.util.Random;
public class Asteroid {
	private int xPos, yPos;
	private Color clr;
	static final int DIM = 600;
	private Random r = new Random();
	private int diameter = r.nextInt(50) + 10; 
	private boolean die = false;

	
	public Asteroid(){
		
		xPos = r.nextInt(DIM);
		yPos = r.nextInt(DIM);
		clr = Color.green;
		die = false;
				
	}
	
	public Asteroid(int i){
		xPos = r.nextInt(i);
		yPos = r.nextInt(i);
		clr = Color.red;
		die = false;
			
	}
	//set color for asteroids
	public void setColor(Color color){
			clr = color;
		}
	
	public void draw(Graphics g){
		g.setColor(clr);
		g.fillOval(xPos, yPos, diameter, diameter);
		
				
	}
	//make asteroids
	//	generate a number between -15 to 15
	public void move(int x, int y){
		Random r = new Random();
		xPos += r.nextInt(31) - 15;
		yPos += r.nextInt(31) - 15;
		xPos = x;
		yPos = y;
		}
	
	
	//methods for get location of the asteroid
		public int getX(){
			return xPos;
		}
		
		public int getY(){
			return yPos;
		}
		
		public void remove(){
			
		}
		public int getDia() {
			return diameter;
		}
		public Point getPosition() {
			return new Point(xPos, yPos);		//returns the position of the asteroid
		}
		
		public void setDie(boolean d){
			this.die = d;
		}
		
		public boolean getDie(){
			return die;
		}
		
}	




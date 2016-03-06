//Xingchi Jin
//expected score:150
//do not hard code the value in the definition of the array or arraylist

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;
//import java.util.Iterator;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;



public class Screen extends JPanel implements ActionListener, MouseListener, MouseMotionListener, ComponentListener,KeyListener {
	private  SpaceShip ship ;
	private  Star[] stars ;
	private int dim = 600;
	//arrayList declared
	private  ArrayList<Asteroid> ast = new ArrayList<Asteroid>(dim);
	private int NUM_ASTEROIDS = 15;
	private int NUM_STARS=100;
	private int i;
	private Timer timer;
	private Timer timer_count;
	private Timer timer_ast;

	private Random r = new Random();
	int num = r.nextInt(NUM_ASTEROIDS)+1;
	private int x = 0, y = 0, deltaX = 0, deltaY = 0;
	private int timeLeft = 15;
	private int score = 0;
	private int lives = 3;
	private boolean gameEnd = false;
	private boolean hit = false, collide = false;


	//constructor, construct four spaceships and three stars	
	public Screen(){
			
		stars = new Star[NUM_STARS];
		ship = new SpaceShip();
		for(i = 0;i < NUM_ASTEROIDS;i++)
			ast.add(new Asteroid(dim));
		
		timer = new Timer(300, this);
			
		for(i=0;i < stars.length;i++)
			stars[i] = new Star();


		setPreferredSize (new Dimension( dim, dim));	
		timer.start();
		//set another timer for showing time left
		timer_count = new Timer(1000, this);
		timer_ast = new Timer(95, this);
		timer_count.start();
		timer_ast.start();
		addMouseListener(this);
		addMouseMotionListener(this);
		addComponentListener(this);
		addKeyListener(this);
		setFocusable(true);
		
	}
	
	//request the components to draw themselves	
	public void paintComponent(Graphics g){
		super.paintComponent(g);
		setBackground(Color.black);
	
		//draw 100 stars		
		for(i = 0;i < stars.length;i++)
			stars[i].drawStar(g);
		
		//Draw asteroids
		for(i = 0;i<NUM_ASTEROIDS;i++){
		if(!ast.get(i).getDie()) ast.get(i).draw(g);
				}
		//ship over asteroids
		ship.draw(g, dim);
		//	set the font for the text 
		Font font = new Font("Serif", Font.PLAIN, 96);
		g.setColor(Color.white);
		
		if(hit && lives>0 && timeLeft>0 && ship.getShoot()){
			g.setFont(new Font("TimesRoman", Font.PLAIN, 30)); 
			g.drawString("HIT!", 200, 200);
			hit = false;
		}
		
		//Print text 
		if (lives == 0 || timeLeft <= 0){
	    	  g.drawString("Score: " + score, 20, 45);
	    	  g.drawString("Life: " + lives, 20, 60);
	    	  g.drawString("Time Remain: " + timeLeft, 20, 75);
	    	  g.setFont(new Font("TimesRoman", Font.PLAIN, 50)); 
	    	  g.drawString("Game Over", 250, 300);
	    	  removeMouseListener(this);
	    	  removeMouseMotionListener(this);
	    	  timer.stop();
	    	  timer_ast.stop();
	    	  timer_count.stop();
	    } else {
	    	  g.drawString("Score: " + score, 20, 45);
	    	  g.drawString("Life: " + lives, 20, 60);
	    	  g.drawString("Time Remain: "+ timeLeft, 20, 75);
	    }   
					
		
	}
	

	public static void main(String[] args) {
		JFrame frame = new JFrame ("SpaceShip");
	    frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);
		Screen screen = new Screen();
	    frame.getContentPane().add(screen);
	    frame.pack();
	    frame.setVisible(true);
		
	}

	public void actionPerformed (ActionEvent e){
		
		Random r = new Random(); 		
		dim = this.getWidth();
					
//		move only 30 percent of the asteroids
		for(i = 0;i< NUM_ASTEROIDS; i++){
			//initailize the location of each asteroid
			x = ast.get(i).getX();
			y = ast.get(i).getY();
			//gen deltaX, deltaY between -15 and 15
			deltaX = r.nextInt(31) - 15;
			deltaY = r.nextInt(31) - 15;
			x += deltaX;
			y += deltaY;
			int n = r.nextInt(10);				
			if (n <= 2){		
				ast.get(i).move(x, y);
			}			
		}
		//control timer_count
		if(e.getSource().equals(timer_count)){
			timeLeft-=1;
			if(timeLeft<=0){
				timeLeft=0;
				gameEnd=true;
				removeMouseListener(this);
				removeMouseMotionListener(this);
				removeComponentListener(this);
				timer.stop();
				timer_count.stop();	
				timer_ast.stop();
				
			}
			repaint();
			
		}
//		control timer
		else if(e.getSource().equals(timer)){
			
			  if (lives > 0 && collide){
					lives --;   
				   } 			   
				   if (lives==0) {
					   timer_count.stop();
					   timer.stop();
					   timer_ast.stop();
				   }
				   repaint();
		}
//		control timer_ast
		
		else if (e.getSource().equals(timer_ast)){
			for(i=0;i<NUM_ASTEROIDS;i++){
				   double astHitX = ast.get(i).getPosition().x ;
				   double astHitY = ast.get(i).getPosition().y ;
				   int r1 = ast.get(i).getDia();
				   double shipY = ship.getPosition().y;
				   double shipX = ship.getPosition().x;
				   
				   
				   //conditions for collision
				   if(!ast.get(i).getDie() && (shipX -25  < astHitX && astHitX < shipX + 25 )
						   && (shipY - 25< astHitY && astHitY < shipY + 25)){
					 //removes asteroid when collision
					   ast.get(i).setDie(true);
					 //lives - 1 after the collison
					   lives--;	
					   
//					   set different colors for Spaceship in its second life and third life
					   if (lives == 2){
						   ship.setColor(Color.yellow);
					   } if (lives == 1){
						   ship.setColor(Color.red);
					   }
					   break;
					   
				   }
				   
				   
				   //conditions for shooting
				   if((!ast.get(i).getDie() && astHitX>=shipX&& astHitY <= shipY && shipY <= astHitY + 0.3*2*r1 && ship.getShoot()==true) ||
						   (!ast.get(i).getDie() && astHitY+0.7*2*r1 <= shipY  
					   	   && shipY <= astHitY+2*r1&& astHitX>=shipX && ship.getShoot() == true)){
					   		ast.get(i).setDie(true);
					   		   score += 1;
					   		   hit = true;
					   		   break;
					   	   }
//
				   else if(!ast.get(i).getDie()&& astHitX>=shipX && astHitY + 0.3*2*r1 < shipY 
						   && shipY < astHitY + 0.7*2*r1 && ship.getShoot() == true){
					   ast.get(i).setDie(true);
					   score += 3;
					   hit = true;
					   break;
				   }				   
			   }
			 		   
			   repaint();
			
		   }

		}
	
	public void mouseClicked(MouseEvent e) {		
		repaint();
	}
	
	public void mouseEntered(MouseEvent e) {}
	
	public void mouseExited(MouseEvent e) {}
	
	public void mousePressed(MouseEvent e) {
		ship.setShooting(true);
//		int ship_x1 = e.getX();
//		int ship_y1 = e.getY();
		System.out.println("Start shooting");

		repaint();
	}
	
	//move along with mouse
	public void mouseMoved(MouseEvent e){
	
		ship.move(e.getX() - 20,e.getY() - 20);		
		repaint();
	}
	
	public void mouseDragged(MouseEvent e){
		ship.move(e.getX(),e.getY());
		ship.setShooting(true);
		System.out.println("Keep shooting");
		repaint();
	}
	
	//stop shooting once release
	public void mouseReleased(MouseEvent e) {
		ship.setShooting(false);
		hit = false;
		System.out.println("stop shooting");
		//ship.move(e.getX(),e.getY());

		repaint();
	}
	
	public void componentHidden(ComponentEvent e){
		
	}
	
	public void componentMoved(ComponentEvent e){
		
	}
	
	
	//resize the screen
	public void componentResized(ComponentEvent e) {
		dim = this.getWidth();
		for(i=0;i < stars.length;i++){
			stars[i].move(dim);
		}
		repaint();
		
	}
	
	public void componentShown(ComponentEvent e){
		
	}
	

	
	public void keyPressed(KeyEvent e){
		if(e.getKeyCode() == KeyEvent.VK_SPACE){
			ship.setShooting(true);
			repaint();
		}
	}
	
	@Override
	public void keyReleased(KeyEvent e) {
		if(e.getKeyCode() == KeyEvent.VK_SPACE){
			ship.setShooting(false);
			repaint();
		}
		
	}
	
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}	
	}
	 






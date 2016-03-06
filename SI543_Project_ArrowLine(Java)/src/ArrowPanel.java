//Xingchi Jin
//do not hard code the value in the definition of the array or arraylist

import javax.swing.*;
import java.awt.*;
//import java.util.Iterator;
import java.awt.event.*;
import java.util.Random;
public class ArrowPanel extends LinePanel implements KeyListener{
	private ImageIcon upImg, downImg, leftImg, rightImg;
	private final int DIM = 600;
	private int x0, y0;
	private String key = "null";
	private int move = 5;
	private Image dis;


	public ArrowPanel() {
		// TODO Auto-generated constructor stub
		x0 = DIM/2;
		y0 = DIM/2;
		
		setBackground(Color.white);
		upImg = new ImageIcon("images/arrow-up.png");
		downImg = new ImageIcon("images/arrow-down.png");
		leftImg = new ImageIcon("images/arrow-left.jpeg");
		rightImg = new ImageIcon("images/arrow-right.jpeg");
		addKeyListener(this);
//		timer = new Timer(100, this);
//		timer.start();
		dis = upImg.getImage();
		
	}
	@Override
	protected void paintComponent(Graphics g){
		super.paintComponent(g); 

		g.drawImage(dis, x0, y0, null);

		
		
	}
		


	private void drawImage(Image dis2) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyPressed(KeyEvent e) {
		// TODO Auto-generated method stub
		System.out.println(e.getKeyCode());
		switch(e.getKeyCode()){
		case KeyEvent.VK_UP:
			key="up";
			dis = upImg.getImage();
			y0 = y0 - move;
			System.out.println("vkup");
			repaint();			
			break;
		case KeyEvent.VK_DOWN:
			key="down";
			dis = downImg.getImage();
			y0= y0 + move;
			System.out.println("vkdown");
			repaint();
			break;
		
		case KeyEvent.VK_LEFT:
			key = "left";
			dis = leftImg.getImage();
			x0 = x0 - move;
			System.out.println("vkleft");
			repaint();
			break;
			
		case KeyEvent.VK_RIGHT:
			key = "right";
			dis = rightImg.getImage();
			x0 = x0 + move;
			System.out.println("vkright");

			repaint();
			break;
			
		case KeyEvent.VK_SPACE:
			key="space";
			System.out.println("vkspace");
			x0=DIM/2;
			y0=DIM/2;
			Random r = new Random();
			int n = r.nextInt(4) + 1;

			
			switch(n){	
			case 1:
				dis = upImg.getImage();
//				g.drawImage(rightImg.getImage(), DIM/2, null);
				System.out.println(0);
				break;
				
			case 2:
				dis = downImg.getImage();
//				g.drawImage(leftImg.getImage(), xCenter - 15, yCenter - 15, null);
				System.out.println(1);
				break;
				
			case 3:
				dis = leftImg.getImage();
				System.out.println(2);
				break;
				
			default:
				dis = rightImg.getImage();
				System.out.println("default!!!!!!!!!!!!!!");
				break;
			}
			
			
			repaint();
//			key = "none";
			break;
			
		default:
//			key="other";
			System.out.println("vkother");
			break;
		}
		
	}

	@Override
	public void keyReleased(KeyEvent e) {
		// TODO Auto-generated method stub
//		timer.stop();
		
	}

	

}


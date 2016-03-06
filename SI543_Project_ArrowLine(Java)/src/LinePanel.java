//Xingchi Jin
//expected score:150
//do not hard code the value in the definition of the array or arraylist

import javax.swing.*;
import java.awt.*;
//import java.util.Iterator;
import java.awt.event.*;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;
public class LinePanel extends JPanel implements MouseListener, MouseMotionListener{

	private Point point1, point2;
	private final int DIM = 600;
//	boolean MousePress = false;
//	boolean MouseStop = false;
	private int flagMDragged=0, flagMPressed=0;
	
	public LinePanel() {
		point1 = new Point();
		point2 = new Point();
		setPreferredSize (new Dimension(DIM, DIM));
		setBackground(Color.white);
		addMouseListener(this);
		addMouseMotionListener(this);

}
	@Override
	protected void paintComponent(Graphics g){
		super.paintComponent(g); //what does it mean???
//		setBackground(Color.black);
		if(flagMDragged==1){
		System.out.print("bg color!!");		
		g.setColor (Color.black);
		g.drawLine(point1.x, point1.y, point2.x, point2.y);
		}
					
	}
			


	
	public static void main (String[] args)
	{
		JFrame frame = new JFrame ("LinePanel");
		frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);

		LinePanel panel = new LinePanel();

		frame.getContentPane().add(panel);
		frame.pack();
		frame.setVisible(true);
	}


	@Override
	public void mouseDragged(MouseEvent e) {
		flagMDragged=1;
		point2.setLocation(e.getX(), e.getY());
		repaint();		
	}

	@Override
	public void mouseMoved(MouseEvent e) {
		
	}

	@Override
	public void mouseClicked(MouseEvent e) {		
	}

	@Override
	public void mousePressed(MouseEvent e) {
		flagMPressed=1;
		double mouseX = e.getX();
		double mouseY = e.getY();
//		MousePress = true;
//		set location for point 1
		point1.setLocation(mouseX, mouseY);
//		point2.setLocation(mouseX, mouseY);
		repaint();		
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		double mouseX = e.getX();
		double mouseY = e.getY();
//		MousePress = true;
//		set location for point 1
		point2.setLocation(mouseX, mouseY);
		repaint();				
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	

}

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class ArrowTester {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		JFrame frame = new JFrame ("ArrowPanel");
		frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);
		ArrowPanel panel = new ArrowPanel();
		
		frame.getContentPane().add(panel);
		frame.pack();
		frame.setVisible(true);
		panel.setFocusable(true);
		panel.requestFocusInWindow();


	}

}

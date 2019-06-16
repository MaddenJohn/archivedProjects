import java.awt.Color;
//import java.applet.Applet;
import java.awt.*;
import java.awt.event.*;
import javax.swing.JApplet;

public class Game extends JApplet implements KeyListener, FocusListener, MouseListener {

	/**
	 * 
	 */
	private static final long serialVersionUID = 5149737360216821718L;
	int size;
	Player p1, p2;
	boolean focus, drawn;
	boolean game;
	Graphics p;
	Image background;
	Dimension dim;
	boolean[][] walls;
	int tempCode;
	int speed;
	boolean selectedMode;
	boolean debug = false;

	public void init() {
		setSize(1000, 600);
		print("initalizing");
		addKeyListener(this);
		addFocusListener(this);
		addMouseListener(this);
		setFocusable(true);

		speed = 5; // larger number is slower
		p1 = new Player(775, 325, Direction.LEFT, "player 1", true);
		p2 = new Player(225, 325, Direction.RIGHT, "player 2", true);
		size = 5;
		game = false;
		tempCode = 0;
		dim = getSize();
		background = createImage(dim.width, dim.height);
		p = background.getGraphics();
		selectedMode = false;
		titleScreen();
		walls = new boolean[dim.width / size + 2][dim.height / size + 2];
		
	}

	public void paint(Graphics g) {
		if (!selectedMode){
			repaint();
		}
		else if(game){
			if (!drawn) {
				drawn = true;
				background(p);
			}
			delay(speed);
			p1.update(size, walls);
			drawNewPos(1);
			p2.update(size, walls);
			drawNewPos(2);
			if (game)
				repaint(); 
		}
		g.drawImage(background, 0, 0, this);
	}

	public void drawNewPos(int pNum) {
		Player player;
		Player other;
		int endNum;
		if (pNum == 1) {
			player = p1;
			other = p2;
			endNum = 2;
			p.setColor(Color.red);
		} else {
			player = p2;
			other = p1;
			endNum = 1;
			p.setColor(Color.blue);
		}
		int x = player.getPosition_x();
		int y = player.getPosition_y();
		if (x < 1000 && y < 600 && x >= 0 && y >= 0 && !walls[x / size][y / size]) {
			drawObject(p, x, y, size);
			walls[x / size][y / size] = true;
		} else {
			if (!tie())
				other.win();
			else
				endNum = 0;
			endgame(p, endNum);
			p.setColor(Color.cyan);
			drawObject(p, x+1, y+1, size-2);
		}
	}

	public boolean tie() {
		if (p1.getPosition_x() == p2.getPosition_x() && p1.getPosition_y() == p2.getPosition_y())
			return true;
		else
			return false;
	}

	public void keyPressed(KeyEvent e) {
		
		
		int keyCode = e.getKeyCode();
		print( Integer.toString(keyCode));
		if (okChange(e, keyCode, tempCode))
			switch (keyCode) {
			case KeyEvent.VK_DOWN:
				p1.setDirection(Direction.DOWN);
				break;
			case KeyEvent.VK_UP:
				p1.setDirection(Direction.UP);
				break;
			case KeyEvent.VK_RIGHT:
				p1.setDirection(Direction.RIGHT);
				break;
			case KeyEvent.VK_LEFT:
				p1.setDirection(Direction.LEFT);
				break;

			case KeyEvent.VK_S:
				p2.setDirection(Direction.DOWN);
				break;
			case KeyEvent.VK_W:
				p2.setDirection(Direction.UP);
				break;
			case KeyEvent.VK_D:
				p2.setDirection(Direction.RIGHT);
				break;
			case KeyEvent.VK_A:
				p2.setDirection(Direction.LEFT);
				break;

			case KeyEvent.VK_R:
				restart();
				break;
			}
		if (okChange(e, keyCode, tempCode))
			tempCode = keyCode;

	}

	// basically, do not let the direction change to the backwards of the
	// currently moving direction
	public boolean okChange(KeyEvent e, int keyCode, int tempCode) {
		if (keyCode != tempCode) {
			if (keyCode == tempCode + 2 || keyCode == tempCode - 2)
				return false;
			if (keyCode == 65 && tempCode == 68 || keyCode == 68 && tempCode == 65)
				return false;
			if (keyCode == 87 && tempCode == 83 || keyCode == 83 && tempCode == 87)
				return false;
		}
		if (tempCode == 0) {
			if (keyCode == 39)
				return false;
			if (keyCode == 65)
				return false;
		}
		return true;
	}

	public void keyTyped(KeyEvent e) {
	}

	public void delay(double n) {
		long startDelay = System.currentTimeMillis();
		long endDelay = 0;
		while (endDelay - startDelay < n)
			endDelay = System.currentTimeMillis();
	}

	public void focusGained(FocusEvent evt) {
		focus = true;
	}

	public void focusLost(FocusEvent evt) {
		focus = false;
	}

	public void titleScreen() {
		p.setColor(Color.black);
		p.fillRect(0, 0, dim.width, dim.height);
		Font title = new Font("Times New Roman", Font.BOLD, 72);
		p.setFont(title);
		p.setColor(Color.white);
		p.drawString("TRON", 350, 325);
		p.setColor(Color.blue);
		Font desc = new Font("Times New Roman", Font.BOLD, 36);
		p.setFont(desc);
		p.drawString("Player 1 - WASD", 325, 475);
		p.setColor(Color.red);
		p.drawString("Player 2 - Arrows", 325, 550);
		p.setColor(Color.black);
		
		p.setColor(Color.white);
		p.fillRect(180, 100, 200, 100);
		p.fillRect(580, 100, 200, 100);
		p.setColor(Color.black);
		p.drawString("P Vs P", 225, 160);
		p.setColor(Color.black);
		p.drawString("P Vs C", 625, 160);

	}

	public void update(Graphics g) {
		paint(g);
	}

	public void drawObject(Graphics p, int x, int y, int size) {
		p.fillRect(x, y, size, size);
	}

	public void endgame(Graphics p, int winner) {
		delay(5);
		Font title = new Font("Times New Roman", Font.BOLD, 72);
		p.setFont(title);
		p.setColor(Color.white);
		p.drawString("Game Over", 300, 100);
	

		if (winner == 2)
			p.drawString("Blue Wins!!", 300, 200);
		else if (winner == 1)
			p.drawString("Red Wins!!", 300, 200);
		else if (winner == 0)
			p.drawString("Tie Game!!", 300, 200);

		Font desc = new Font("Times New Roman", Font.BOLD, 36);
		p.setFont(desc);
		p.setColor(Color.blue);
		p.drawString("Player 1 - WASD", 325, 475);
		p.setColor(Color.red);
		if(!p1.getAI())
			p.drawString("Player 2 - Arrows", 325, 550);
		drawScore(p, p2.getScore(), p1.getScore());
		game = false;
		p.setColor(new Color(0, 100, 0));
		p.fillRect(750, 50, 100, 50);
		p.setColor(Color.black);
		Font button = new Font("Times New Roman", Font.BOLD, 12);
		p.setFont(button);
		p.drawString("Press R to restart", 760, 70);
		Font small = new Font("Times New Roman", Font.BOLD, 12);
		p.setFont(small);
		p.drawString("or click button", 760, 85);	
	}

	public void background(Graphics p) {
		p.setColor(Color.black);
		p.fillRect(0, 0, dim.width, dim.height);
		p.setColor(new Color(0, 100, 0));
		for (int k = 0; k < dim.width; k += 50) {
			p.drawLine(k, 0, k, dim.height);
			p.drawLine(0, k, dim.width, k);
		}
	}

	public void keyReleased(KeyEvent e) {
		print("key released");
	}

	public void restart() {
		p1.initialize();
		p2.initialize();
		tempCode = 0;
		game = true;
		for (int r = 0; r <= dim.height / size; r++) {
			for (int c = 0; c <= dim.width / size; c++) {
				walls[c][r] = false;
			}
		}
		background(p);
		repaint();
	}

	public void drawScore(Graphics p, int b, int r) {
		Font score = new Font("Times New Roman", Font.BOLD, 32);
		p.setFont(score);
		p.setColor(Color.black);
		p.fillRect(51, 6, 48, 42);
		p.fillRect(901, 6, 48, 42);
		p.setColor(Color.blue);
		p.drawString(String.valueOf(b), 67, 37);
		p.setColor(Color.red);
		p.drawString(String.valueOf(r), 917, 37);
	}

	@Override
	public void mouseClicked(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mousePressed(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseReleased(MouseEvent e) {
		if (!game && e.getX() > 750 && e.getX() < 850 && e.getY() > 50 && e.getY() < 100){
			print("clicked restart");
			restart();
		}
		else if (!selectedMode && e.getX() > 180 && e.getX() < 380 && e.getY() > 100 && e.getY() < 200){
			p1.setAI(false);
			p2.setAI(false);
			selectedMode = true;
			game = true;
			print("clicked PVP");
			repaint();
		}
		else if (!selectedMode && e.getX() > 580 && e.getX() < 780 && e.getY() > 100 && e.getY() < 200){
			p2.setAI(false);
			selectedMode = true;
			game = true;
			print("clicked PVC");
			repaint();
		}
		else 
			print("bad click");
		
		
	}
	
	private void print(String message){
		if(debug)
			System.out.println(message);
	}

}

import java.util.Random;

public class Player {
	private int position_x;
	private int position_y;
	private int init_x;
	private int init_y;
	private Direction init_d;
	private Direction direction;
	private int score;
	private String name;
	private boolean AI;

	public Player(int x, int y, Direction d, String name, boolean AI) {
		init_x = x;
		init_y = y;
		init_d = d;
		setPosition_x(x);
		setPosition_y(y);
		setDirection(d);
		score = 0;
		this.name = name;
		this.AI = AI;
	}

	public boolean getAI() {
		return AI;
	}
	
	public void setAI(boolean value) {
		AI = value;
	}

	public void initialize() {
		position_x = init_x;
		position_y = init_y;
		direction = init_d;
	}

	public int getScore() {
		return score;
	}

	public void win() {
		score++;
	}

	public void setDirection(Direction d) {
		if(!AI)
			this.direction = d;
	}

	public Direction getDirection() {
		return direction;
	}

	public void updatePosition(int size) {
		switch (direction) {
		case RIGHT:
			position_x += size;
			break;
		case LEFT:
			if (position_x >= size)
				position_x -= size;
			break;
		case UP:
			if (position_y >= size)
				position_y -= size;
			break;
		case DOWN:
			position_y += size;
			break;
		}
	}

	public void computerUpdate(int size, boolean[][] walls) {
		boolean chosen = false;
		int init_x = position_x;
		int init_y = position_y;
		int tries = 30;
		while (!chosen && tries > 0) {
			chosen = true;
			updatePosition(size);
			if (bad_pick(position_x, position_y, walls, size)) {
				compGetNewDir();
				chosen = false;
				tries--;
				if (tries > 1)
					updatePosition(init_x, init_y);
			}
		}
	}

	public void update(int size, boolean[][] walls) {
		if (AI)
			computerUpdate(size, walls);
		else
			updatePosition(size);
	}

	public void printPos() {
		System.out.println(name + "  x: " + position_x + " y: " + position_y);
	}

	private void compGetNewDir() {
		Random r = new Random();
		int num = r.nextInt(100);
		if (num < 25)
			direction = Direction.LEFT;
		else if (num < 50)
			direction = Direction.RIGHT;
		else if (num < 75)
			direction = Direction.UP;
		else
			direction = Direction.DOWN;

	}

	private boolean bad_pick(int x, int y, boolean[][] walls, int size) {
		if (x >= 1000 || x < 0 || y >= 600 || y < 0)
			return true;
		return walls[x / size][y / size];
	}

	public void updatePosition(int x, int y) {
		setPosition_x(x);
		setPosition_y(y);
	}

	public int getPosition_x() {
		return position_x;
	}

	public void setPosition_x(int position_x) {
		this.position_x = position_x;
	}

	public int getPosition_y() {
		return position_y;
	}

	public void setPosition_y(int position_y) {
		this.position_y = position_y;
	}

}

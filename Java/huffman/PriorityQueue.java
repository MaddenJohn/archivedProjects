/*  Student information for assignment:
 *
 *  On our honor, Jonathan Madden and Khiem Tang, this programming assignment is our own work
 *  and we have not provided this code to any other student.
 *
 *  Number of slip days used: 1
 *
 *  Student 1: Jonathan Madden
 *  UTEID: jm76685
 *  email address: johnmadden4477@yahoo.com
 *  Grader name: Donghyuk
 *  Section number: 51740
 *
 *  Student 2: Khiem Tang
 *  UTEID: klt2399
 *  email address: tang.khiem@yahoo.com
 *  Grader name: Donghyuk
 *  Section number: 51740
 */

import java.util.LinkedList;

public class PriorityQueue<E> {
	// Instance variables
	private LinkedList<E> con;

	public PriorityQueue() {
		// Container defined in constructor
		con = new LinkedList<E>();
	}

	public int size() {
		// Returns container size
		return con.size();
	}

	public TreeNode dequeue() {
		// Removes first element from LinkedList
		return (TreeNode) con.remove(0);
	}

	public void enqueue(TreeNode node) {
		// Enqueues a treeNode to the queue
		con.add(getIndex(node), (E) node);
	}

	private int getIndex(TreeNode node) {
		int index = 0;
		// Runs through each index of container
		for (E e : con) {
			TreeNode temp = (TreeNode) e;
			// compareTo called to determine sorted location
			if (temp.compareTo(node) > 0) {
				return index;
			}
			index++;
		}
		return index;
	}

	public E front() {
		// Returns first element of container
		return con.get(0);
	}

	public boolean isEmpty() {
		// Checks if container size is zero
		return size() == 0;
	}

	public String toString() {
		String result = "";
		// Runs through each index of container and prints node
		for (E e : con) {
			TreeNode temp = (TreeNode) e;
			System.out.println(temp);
		}
		return result;
	}

	public void printTree() {
		// Runs printHelper method to print tree.
		printHelper((TreeNode) this.con.getFirst());
	}

	public int x = 0;

	private void printHelper(TreeNode n) {
		// Traverses tree and prints each node / leaf
		while (n != null && x < 26) {
			x++;
			System.out.println(n);
			printHelper(n.getLeft());
			printHelper(n.getRight());
		}
		// Returns null if tree is empty
		System.out.println("null");
	}

}

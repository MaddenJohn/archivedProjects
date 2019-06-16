/*
 * Data stucture used to create the huffman tree.
 * Only change here is using a String instead of a character for letters.
 * Credit to http://cs.smith.edu/dftwiki/index.php/CSC212_Huffman_Ecoding_in_Java 
 * Website used for getting the huffman codes algorithm.
 */
public class Node implements Comparable<Node> {
                public String letters;                             // the letter from the string, or '#' if inner node, modified from char
                public int Id;                                  // unique Id (used to generate DOT graph)       
                public int freq;                                // counts number of occurrences
                public Node left;                               // pointer to left child, if any
                public Node right;                              // pointer to right child, if nay
                
                Node( String l, int f, Node lft, Node rt ) {
                        letters = l; freq = f; left = lft; right = rt; 
                }
                /**
                 * returns whether node is a leaf.
                 * @return true if leaf, false otherwise.
                 */
                public boolean isLeaf() { return left==null && right==null; }
                @Override
                /**
                 * compareTo: needed because nodes will be kept in priority queue that
                 * keeps node with smallest freq value at the root. 
                 */
                public int compareTo(Node o) {
                        return freq - ((Node) o).freq;
                }
        }
import java.util.ArrayList;
import java.util.Scanner;

public class Game {

	public static void main(String[] args) {
		Scanner s = new Scanner(System.in);
		int games = s.nextInt();
		ArrayList<String> Llines = new ArrayList<String>();
		for(int i = 0;i<=games;i++)
			Llines.add(s.nextLine());
		
		
		String result = "";
		String lose = "I am screwed\n";
		String win = "I will win\n";
		for(int i = 0;i<games;i++){//System.out.println(Llines.get(i+1));
			Scanner s1 = new Scanner(Llines.get(i+1));
			//int test = s1.nextInt();
			int	n1 = Integer.parseInt(s1.next());
			int	n2 = Integer.parseInt(s1.next());
			int	k1 = Integer.parseInt(s1.next());
			int	k2 = Integer.parseInt(s1.next());
				//System.out.println(n1);
			
			while(n1>0&&n2>0){
				System.out.println(n1);
				System.out.println(n2);
				n1-=1;
				if(n1==0)
					result+=lose;
				else{
					n2-=1;
					if(n2==0)
						result+=win;
				}
				System.out.println(n1);
				System.out.println(n2+"\n");
			}
			
		}
		System.out.println(result);
		

	}

	private static int parseInt(String next) {
		// TODO Auto-generated method stub
		return 0;
	}

}

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
public class Gender {

	public static void main(String[] args) {
		//System.out.println("test");
		Scanner s = new Scanner(System.in);
		
		int lines = s.nextInt();
		ArrayList<String> Llines = new ArrayList<String>();
		for(int i = 0;i<=lines;i++)
			Llines.add(s.nextLine());
		
		
		ArrayList<String> Test = new ArrayList<String>(Arrays.asList("she"));
		
		ArrayList<String> Flist = new ArrayList<String>();
		ArrayList<String> Mlist = new ArrayList<String>();
		Flist.add("she");
		Flist.add("her");
		Flist.add("hers");
		Flist.add("herself");
		Flist.add("woman");
		Flist.add("women");
		Flist.add("wife");
		Flist.add("sister");
		Flist.add("daughter");
		Flist.add("mother");
		Flist.add("girl");
		Flist.add("She");
		Flist.add("Her");
		Flist.add("Hers");
		Flist.add("Herself");
		Flist.add("Woman");
		Flist.add("Women");
		Flist.add("Wife");
		Flist.add("Sister");
		Flist.add("Daughter");
		Flist.add("Mother");
		Flist.add("Girl");
		
		Mlist.add("he");
		Mlist.add("him");
		Mlist.add("his");
		Mlist.add("himself");
		Mlist.add("man");
		Mlist.add("men");
		Mlist.add("husband");
		Mlist.add("brother");
		Mlist.add("son");
		Mlist.add("father");
		Mlist.add("boy");
		Mlist.add("He");
		Mlist.add("Him");
		Mlist.add("His");
		Mlist.add("Himself");
		Mlist.add("Man");
		Mlist.add("Men");
		Mlist.add("Husband");
		Mlist.add("Brother");
		Mlist.add("Son");
		Mlist.add("Father");
		Mlist.add("Boy");
		
		
		
		
		
		
		
		
		// "he and she", "him and her", "his and hers", "himself and herself", "man and woman", "men and women", 
		//"husband and wife", "brother and sister", "son and daughter", "father and mother", and "boy and girl".
		String result = "";
		int counter = 0;
		while(counter<=lines){
			counter++;
			Scanner s1 = new Scanner(Llines.get(counter-1));
			while(s1.hasNext()){
				String test = s1.next();
				if(Flist.contains(test)){
					int index = Flist.indexOf(test);
					result+=(Mlist.get(index)) + " ";
				}
				else if(Mlist.contains(test)){
					int index = Mlist.indexOf(test);
					result+=(Flist.get(index) + " ");
				}
				else {result+=test+ " ";}	
			}
			
			
			//result=result.substring(0, result.length()-2);
			result+="\n";
			
		}
		System.out.println(result);
		
		

	}

}

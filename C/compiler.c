#include <stdint.h> 
#include "stdio.h"


int main (int argc, char* argv[]) { 
int c = argc;
int element = 1;
int stackCount = 0;
int r10null = 1;
int numPop = 9456;
int numCount = 0;
fprintf(stdout," .globl compute\ncompute:\n");
	while( c > 1 ) // argc = #arguments + 1 
	{
		int stackChange;
		if(is_valid_input(argv[element])){
			stackCount++;
			int overflow = 0;
			if(element ==1){
				if(is_var(argv[element])){
					if(*argv[element]=='x')
						fprintf(stdout,"  movq  %rdi, %rax\n");
					if(*argv[element]=='y')
						fprintf(stdout,"  movq  %rsi, %rax\n");
					if(*argv[element]=='z')
						fprintf(stdout,"  movq  %rdx, %rax\n");
				}
				else if(is_num(argv[element])){
					fprintf(stdout,"  movq  $%s, %rax\n",(argv[element]));
				}
				else{
					fprintf(stderr,"Invadid input. Enter two numbers before operation\n");
					return 0;
					}
			}
			else{
				if(is_op(argv[element])){
					if(stackCount>2){
						if(is_num(argv[element-1])&&(stackCount==3||stackCount>3)){
							long long temp2;
							int position = element-1;
							if(stackCount>3)
								position = element-stackCount+stackCount-2;
							sscanf(argv[element-1],"%lld",&temp2);
							overflow = (temp2>=2147483647)|| (temp2<=-2147483646);
						}
						if(stackCount>3&&r10null||(stackCount==3&&overflow)){
							r10null=0;
							if(is_num(argv[element-1])){
								fprintf(stdout,"  movq  $%s, %r10\n",(argv[element-1]));
							}
							else if(is_var(argv[element-1])){
								if(*argv[element-1]=='x')
									fprintf(stdout,"  movq  %rdi, %r10\n");
								if(*argv[element-1]=='y')
									fprintf(stdout,"  movq  %rsi, %r10\n");
								if(*argv[element-1]=='z')
									fprintf(stdout,"  movq  %rdx, %r10\n");
							}
							stackChange=element-stackCount;
						}
						if(stackCount>3&&!r10null&&overflow){
							fprintf(stdout,"  movq  $%s, %r11\n",(argv[element-1]));
						}
					
						if(numCount==numPop&&numPop!=0)
							fprintf(stdout,"  popq  %r11\n");
					

						char c = *argv[element];
						switch(c){
							case '+':
								fprintf(stdout,"  addq  ");		
								break;
							case '*':
								fprintf(stdout,"  imulq ");		
								break;
							case '-':
								fprintf(stdout,"  subq  ");		
								break;
						}
						if(stackCount>3&&!r10null&&overflow){
							fprintf(stdout,"%r11, %r10\n");
						}
						else if(numCount==numPop&&numPop!=0&&numPop!=9456){
							fprintf(stdout,"%r11, %r10\n");
							if(c=='-')
									fprintf(stdout,"  imulq $-1, %r10\n");
							numPop--;
							if(stackCount==3)
								fprintf(stdout,"  addq  %r10, %rax\n");

						}
						else if(stackCount ==3&&r10null&&numCount !=numPop||((numCount==numPop)&&numPop==9456)&&!overflow){	
							if(is_num(argv[element-1])){
								fprintf(stdout,"$%s, %rax\n",(argv[element-1]));
							}
							else if(is_var(argv[element-1])){
								if(*argv[element-1]=='x')
									fprintf(stdout,"%rdi, %rax\n");
								if(*argv[element-1]=='y')
									fprintf(stdout,"%rsi, %rax\n");
								if(*argv[element-1]=='z')
									fprintf(stdout,"%rdx, %rax\n");
							}
						}
						else if(stackCount>3&&!r10null&&numCount !=numPop||((numCount==numPop)&&numPop==9456)){
							int position = stackCount-2+stackChange; 
						
							if(is_num(argv[position])){
								fprintf(stdout,"$%s, %r10\n",(argv[position]));
							}
							else if(is_var(argv[position])){
								if(*argv[position]=='x')
									fprintf(stdout,"%rdi, %r10\n");
								if(*argv[position]=='y')
									fprintf(stdout,"%rsi, %r10\n");
								if(*argv[position]=='z')
									fprintf(stdout,"%rdx, %r10\n");
							}	
							if(c=='-')
									fprintf(stdout,"  imulq $-1, %r10\n");
						}
						else if(stackCount==3&&!r10null&&numCount!=numPop||((numCount==numPop)&&numPop==0)||(stackCount==3&&overflow)){
							fprintf(stdout,"%r10, %rax\n");
							r10null=1;
							numPop = 9456;
						}
				


					}
					else{
						fprintf(stderr,"Not enough numbers. An operation needs 2 numbers on stack\n");
					return 0;
					}
					if(numCount>0)
						numCount--;
					stackCount-=2;
				}
				else {
				
					if(numCount>0)
						numCount++;
					if(!r10null){
					
						if(numPop == 9456){
							numPop=0;
						}
						numPop++;
						r10null=1;
						fprintf(stdout,"  pushq %r10\n");
						if(numCount==0)
							numCount = 1;
					}
					
				}
			}
		}
		else{
			fprintf(stderr,"Invadid input. Enter only numbers, seperate operations, and the variables 'x', 'y', and 'z'\n");
			return 0;		
		}
	

		element++;
		c--;
		if(c==1 &&element>0){
			fprintf(stdout,"  retq\n");
			if(stackCount!=1){
				fprintf(stderr,"Not enough operations. Numbers left on stack\n");
				return 0;
			}
		}
	
	}
   
}

int is_valid_input(const char *str)
{
   if (!*str) //empty strings
       return 0;
   return is_var(str)+is_num(str)+is_op(str);
}

int is_var(const char *str)
{
   if (*str == 'x' ||*str == 'y' ||*str == 'z' ){
	++str;
	if(!*str)
		return 1;
	else 
		return 0;
   }
return 0;

}

int is_num(const char *str)
{
   if(*str=='-') //if negative ignore sign
	++str;

   // check for things other than numbers
   while (*str)
   {
      if (!isdigit(*str))
         return 0;
      else
         ++str;
   }
   return 1;
}

int is_op(const char *str)
{
  if (*str == '+' ||*str == '-' ||*str == '*' ){
	++str;
	if(!*str)
		return 1;
	else 
		return 0;
   }
	return 0;
}


#include<stdio.h>
#define LENGTH (sizeof(a) / sizeof(a[0]))

int main(){
    char *str = "Hello,World";
    char str1[] = "Hello World";

    int length = 0,i = 0;
    while(str1[i]){
     	length += 1; 
        i += 1;
    }
    printf("%d\n",length);
    return 0;
}
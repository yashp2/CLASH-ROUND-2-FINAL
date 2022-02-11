#include "E:\PISB\ff\CREDENZ-02-02-22\CREDENZ-02-02-22-Alpha/sandbox/filter/filter.h"
#include<iostream>
#include<math.h>
using namespace std; 
asdfvdfbd
int main(){
put_filter();

    int n;
    cin>>n;
    int original_n =n;
    int rev=0;
    int sum =0;
    while(n>0){
        int lastdigit = n%10;
        sum =sum + pow(lastdigit,3);
        cout<<"p"<<pow(lastdigit , 3 );
        n=n/10;
        cout<<"s"<<sum<<endl;
    }
    cout<<"sum"<<sum<<endl;
    if(sum==original_n){
        cout<<original_n<<"is armstrong number";
    }
    else{
        cout<<original_n<<" is not armstrong number ";
    }
return 0;
}
#include<iostream>
#include<math.h>
using namespace std; 

int
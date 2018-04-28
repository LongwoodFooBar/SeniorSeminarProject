//Math 345: Homework 7, Problem 4B
//Heather Switzer

#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

int gcd(int a, int b){
    if(a == b)
	return a;
    if(a == 0 || b == 0)
	return 0;
    if(a > b)
	for(int i = b; i > 0; --i)
	    if(b % i == 0 && a % i == 0)
		return i;
    for(int i = a; i > 0; --i)
	if(a % i == 0 && b % i == 0)
	    return i;
}

int main(){
    for(int s = 3; s <= 49; s+=2){
	for(int t = 1; t < s; t+=2){
	    int a = s*t;
	    int b = (s*s - t*t)/2;
	    int c = (s*s + t*t)/2;
	
	    if(a + 2 == c && gcd(a,b) == 1 && gcd(b,c) == 1 && gcd(a,c) == 1){
		cout << s << " " << t << " " << a << " " << b << " " << c << endl;
	    }

	}
    }

    return 0;
}

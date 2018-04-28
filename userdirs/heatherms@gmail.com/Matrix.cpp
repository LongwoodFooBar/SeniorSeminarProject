#include<iostream>
#include<fstream>
using namespace std;

int main(){
	string x = "";
	ofstream file;
	file.open("Matrix.txt");
	for(int i = 0; i < 54; ++i){
		file << "{";
		for(int j = 0; j < 54; ++j){
			cin >> x;
			file << x;
			file << ", ";
			
		}
		file << "}";
	}
	file.close();
	return 0;

}

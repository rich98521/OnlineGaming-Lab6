#include "stdafx.h"
#pragma comment(lib, "wldap32.lib")
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "winmm.lib")
 
#include <stdio.h>
#include "curl\curl.h"
#include <iostream>
#include "string.h"
 
#include <stdlib.h>
#include <sstream>
 
 
using namespace std;
 
int main(void)
{
    //Useful for HTPPS
    //curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, FALSE);
 
    curl_global_init(CURL_GLOBAL_ALL);
    CURL * myHandle = curl_easy_init();
 
    CURLcode result;

	string urlGetScore = "http://52.35.36.25:8888/score/";
	string urlAddScore = "http://52.35.36.25:8888/updatescore";
	string in;
	while (getline(cin, in))
	{
		if (in.substr(0, 3) == "add")
		{
			string name = in.substr(4, std::find(in.begin() + 5, in.end(), ' ') - in.begin() - 4);
			string score = in.substr(in.find(name, 0) + name.size() + 1);
			myHandle = curl_easy_init();
			curl_easy_setopt(myHandle, CURLOPT_URL, urlAddScore.c_str());
			string toAdd = ("name=" + name + "&score=" + score);
			curl_easy_setopt(myHandle, CURLOPT_POSTFIELDS, toAdd.c_str());
			result = curl_easy_perform(myHandle);
			cout << result << endl;
			curl_easy_cleanup(myHandle);
		}
		else if (in.substr(0, 5) == "check")
		{
			string name = in.substr(6);
			myHandle = curl_easy_init();
			curl_easy_setopt(myHandle, CURLOPT_URL, (urlGetScore + name).c_str());
			result = curl_easy_perform(myHandle);
			cout << result << endl;
			curl_easy_cleanup(myHandle);
		}
	}

 
 
    return 0;
}
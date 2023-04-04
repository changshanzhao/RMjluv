#include <iostream>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;
int main()
{
	vector<Mat> myTemplate;
	for (int i = 0; i < 10; i++)
	{
		Mat temp1 = imread(to_string(i) + ".jpg", 0);
		myTemplate.push_back(temp1);
		resize(myTemplate[i], myTemplate[i], Size(30, 30), (0, 0), (0, 0));
		vector<int> compression_params;
		
		compression_params.push_back(IMWRITE_PXM_BINARY);

		compression_params.push_back(1);
		imwrite(to_string(i)+".pgm", myTemplate[i], compression_params);
		
	}
	
	return 0;
}
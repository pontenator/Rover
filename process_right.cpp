#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>

// Camera matrix and distortion coefficients here  
//3755.14957338, 0.0, 1762.30417143, 0.0, 9756.60361797, 1583.03137770, 0.0, 0.0, 1.0
cv::Mat mtx = (cv::Mat_<double>(3, 3) << 1755.14957338, 0.0, 762.30417143, 0.0, 1756.60361797, 583.03137770, 0.0, 0.0, 1.0);

// Distortion coefficients
cv::Mat dist = (cv::Mat_<double>(5, 1) << -0.48424907, -0.06513039, -0.00019235, -0.00162561, 1.85653613);

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
	try
	{
		cv::Mat flipped_img, undist_img, rgb_img;

		// Convert to a CvImage
		cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

		// Flip it
	        cv::flip(cv_ptr->image, flipped_img, 0);

		// Undistort
		cv::undistort(flipped_img, undist_img, mtx, dist);

		// Convert to RGB
		cv::cvtColor(undist_img, rgb_img, cv::COLOR_BGR2RGB);

	        // Save
		cv::imwrite("/home/docker/catkin_ws/src/camera/images/right.jpg", rgb_img);
	}
	catch (cv::Exception& e)
	{
	        ROS_ERROR("OpenCV exception: %s", e.what());
	}
}


int main(int argc, char **argv)
{
	std::cout << "Starting right camera processing node" << std::endl;
	ros::init(argc, argv, "image_processor");
	ros::NodeHandle nh;

	ros::Subscriber image_sub = nh.subscribe("/image_topic_cam2", 1, imageCallback);
	ros::spin();
}

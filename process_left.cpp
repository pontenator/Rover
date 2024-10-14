#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>

// Camera matrix
cv::Mat mtx = (cv::Mat_<double>(3, 3) << 1766.47970139, 0.0, 766.36855923, 0.0, 1768.28898369, 602.99520165, 0.0, 0.0, 1.0);

// Distortion coefficients
cv::Mat dist = (cv::Mat_<double>(5, 1) << -0.48221321, -0.00243748, -0.00008746, -0.00222248, 1.21215652);

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{

	cv::Mat undist_img, flipped_img, rgb_img;

	// Convert to a CvImage
	cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

	// Flip it
        cv::flip(cv_ptr->image, flipped_img, 0);

	// Undistort
	cv::undistort(flipped_img, undist_img, mtx, dist);

	// Convert to RGB
	cv::cvtColor(undist_img, rgb_img, cv::COLOR_BGR2RGB);

	// Save img
	cv::imwrite("/home/docker/catkin_ws/src/camera/images/left.jpg", rgb_img);
}


int main(int argc, char **argv)
{
	std::cout << "Starting left camera processing node" << std::endl;
	ros::init(argc, argv, "image_processor");
	ros::NodeHandle nh;

	ros::Subscriber image_sub = nh.subscribe("/image_topic_cam1", 1, imageCallback);
	ros::spin();
}

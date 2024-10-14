#include <lccv.hpp>
#include <opencv2/opencv.hpp>
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include "sensor_msgs/Image.h"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/opencv.hpp"

int main(int argc, char **argv)
{
    std::cout << "starting camera_node" << std::endl;
    ros::init(argc, argv, "talker");
    ros::NodeHandle nh;
    ros::Publisher chatter_pub = nh.advertise<std_msgs::String>("chatter", 1000);
    ros::Publisher image_pub_cam1 = nh.advertise<sensor_msgs::Image>("image_topic_cam1", 1);
    ros::Publisher image_pub_cam2 = nh.advertise<sensor_msgs::Image>("image_topic_cam2", 1);

    cv::Mat image_cam1, image_cam2;
    lccv::PiCamera cam1, cam2;

    // Cam1 config
    cam1.options->photo_width = 1456;
    cam1.options->photo_height = 1088;
    cam1.options->verbose = true;

    // Cam2 config
    cam2.options->photo_width = 1456;  // 1024 1456
    cam2.options->photo_height = 1088;  // 768, 1088
    cam2.options->verbose = true;

    for(int i = 0; i < 1; i++){
        std::cout << "Capturing from Camera 1: " << i << std::endl;
        if(!cam1.capturePhoto(image_cam1)){
            std::cout << "Camera 1 error" << std::endl;
        }
        cv::imwrite("/home/docker/catkin_ws/src/camera/images/raw_left.jpg", image_cam1);

        std::cout << "Capturing from Camera 2: " << i << std::endl;
        if(!cam2.capturePhoto(image_cam2)){
            std::cout << "Camera 2 error" << std::endl;
        }
        cv::imwrite("/home/docker/catkin_ws/src/camera/images/raw_right.jpg", image_cam2);
    }

    cv_bridge::CvImage cv_image_cam1, cv_image_cam2;
    cv_image_cam1.encoding = "bgr8";
    cv_image_cam1.image = image_cam1;

    cv_image_cam2.encoding = "bgr8";
    cv_image_cam2.image = image_cam2;

    sensor_msgs::ImagePtr ros_image_cam1 = cv_image_cam1.toImageMsg();
    sensor_msgs::ImagePtr ros_image_cam2 = cv_image_cam2.toImageMsg();

    ros::Rate loop_rate(0.1);
    int count = 0;
    while (ros::ok())
    {
        std_msgs::String msg;
        std::stringstream ss;
        ss << "hello world " << count;
        msg.data = ss.str();
        ROS_INFO("%s", msg.data.c_str());
        chatter_pub.publish(msg);

        // Capture and publish images from both cameras
        if(cam1.capturePhoto(image_cam1)){
            cv_image_cam1.image = image_cam1;
            ros_image_cam1 = cv_image_cam1.toImageMsg();
            image_pub_cam1.publish(ros_image_cam1);
        } else {
            ROS_ERROR("Failed to capture image from Camera 1");
        }

        if(cam2.capturePhoto(image_cam2)){
            cv_image_cam2.image = image_cam2;
            ros_image_cam2 = cv_image_cam2.toImageMsg();
            image_pub_cam2.publish(ros_image_cam2);
        } else {
            ROS_ERROR("Failed to capture image from Camera 2");
        }

        ros::spinOnce();
        loop_rate.sleep();
        count++;
    }
}

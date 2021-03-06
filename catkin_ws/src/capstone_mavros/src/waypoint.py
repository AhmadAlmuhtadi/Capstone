#!/usr/bin/env python
import rospy

#import ros message types
import mavros
from mavros import command
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL
from mavros_msgs.msg import State
from sensor_msgs.msg import NavSatFix

from geometry_msgs.msg import PoseStamped

#to run in parallel
import threading


#using global position for sending global waypoints to the land command
#for navigation we use local position

#init method/ constructor, global variables 
class Waypoint(object):
    def __init__(self):
        rospy.init_node("waypoint")
        mavros.set_namespace()
        #callback function for the first subscriber
        self.gps_subscriber  = rospy.Subscriber("mavros/global_position/global", NavSatFix, self.get_gps_coordinate_cb)
        #self.state_subscriber = rospy.Subscriber("mavros/state", State, self.state_cb)
        self.local_position_publisher = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=10)
        self.takeoff_client = rospy.ServiceProxy("mavros/cmd/takeoff", CommandTOL)
        self.arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
        self.set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)
        self.state = State()
        self.done = False
        self.waypoint_list = []
        self.rate = rospy.Rate(20)
        self.next_waypoint = PoseStamped()
        self.latitude = 0
        self.lngitude = 0

    #callback function for the first subscriber (gps_subscriber)
    def get_gps_coordinate_cb(self, msg):
        #with reference to mav frame
        self.latitude = msg.latitude
        self.lngitude = msg.longitude

    #ros service for setting mode
    def set_mode(self, mode="GUIDED"):
        rospy.wait_for_service("mavros/set_mode")
        isModeChanged = self.set_mode_client(custom_mode=mode)
        return isModeChanged
    
    #service for arming
    def arm(self, arming=True):
        rospy.wait_for_service("mavros/cmd/arming")
        return self.arming_client(arming)
        
    #redundant and not used
    #def state_cb(self, data):
    #    self.state = data

    #helper function to create the ros message for setting the waypoint
    def set_position(self, x, y, z):
        self.next_waypoint.pose.position.x = x
        self.next_waypoint.pose.position.y = y
        self.next_waypoint.pose.position.z = z


    #this is run on the second thread in parallel with main
    def publish_waypoint(self):

        rate = rospy.Rate(20)
        while not rospy.is_shutdown() and not self.done:
            #send the waypoint from previous helper function to the publisher
            self.local_position_publisher.publish(self.next_waypoint)
            rate.sleep()

    
    def main(self):
        self.set_mode(mode='GUIDED')
        self.arm()
        #default yaw 1 for heading
        command.takeoff(min_pitch=0, yaw=0, latitude=self.latitude, longitude=self.lngitude, altitude=2)
        rospy.sleep(10)
        self.waypoint_list = [
            [1,3,2],
            [3,1,1],
            [2,2,2]
        ]


        publisher_thread = threading.Thread(target=self.publish_waypoint)
        #start the thread (publish_waypoint) from previous line
        publisher_thread.start()

        #Both while and for loops are running simultaneously to publish the waypoint and set the next.

        #go through all waypoints
        for point in self.waypoint_list:
            #sends one waypoint at a time to set_position
            self.set_position(point[0], point[1], point[2])
            rospy.sleep(10)

        #make true when all waypoints done    
        self.done = True
        
        #reset the previous thread
        publisher_thread.join()

        command.land(min_pitch=0.0, yaw=0, latitude=self.latitude, longitude=self.lngitude, altitude=0.0)


if __name__ == "__main__":
    
    waypoint = Waypoint()
    waypoint.main()

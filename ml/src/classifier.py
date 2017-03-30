import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from svm import SVM

training = False
data_file = 'data.txt'
f = None

class SubAndPub:
    def __init__(self):
        self.n = rospy.init_node('imu_ml')
        self.pub = rospy.Publisher('boundary_collision', String, queue_size=10)
        self.imu_sub = rospy.Subscriber('imu/data', String , self.imu_callback)
        self.classifier = SVM(predictions=True)
        self.time = rospy.Time()

    def imu_callback(self, imu_data):
        d = imu_data.linear_acceleration + imu_data.angular_velocity
        collision = self.classifier.predict(d)
        self.pub.publish(collision)
        if training:
            f.write(d + self.time.get_time())
            


def main():
    a = SubAndPub()
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

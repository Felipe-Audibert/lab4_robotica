import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from  turtlesim.msg import Pose
from  geometry_msgs.msg import Twist, Pose2D


class controler(Node):

    def __init__(self):
        super().__init__('controler')

        self.init_variables()
        self.init_publishers()
        self.init_subscriber()



    def init_publishers(self):
        self.publisher = self.create_publisher(Twist, '/FRA/turtle1/cmd_vel', 10)

        self.timer = self.create_timer(0.5, self.timer_callback)


    def init_subscriber(self):
        self.subscription_pose = self.create_subscription(Pose,'/FRA/turtle1/pose',self.listener_callback,10)
        self.subscription_goal = self.create_subscription(Pose2D,'/FRA/goal',self.goal_callback,10)


    def init_variables(self):
        # pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # objetivo
        self.x_goal = 10.0
        self.y_goal = 5.0

        # erro (objetivo-pose)
        self.x_error = 0.0
        self.y_error = 0.0

        # controlador
        self.p = 0.0
        self.alpha = 0.0
        self.v_max = 2.0
        self.k_w = 1
        self.msg_controle = Twist()
        self.msg_controle.linear.x = 0.0
        self.msg_controle.linear.y = 0.0
        self.msg_controle.linear.z = 0.0
        self.msg_controle.angular.x = 0.0
        self.msg_controle.angular.y = 0.0
        self.msg_controle.angular.z = 0.0


    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.data)
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta


    def goal_callback(self, msg):
        self.x_goal = msg.x
        self.y_goal = msg.y


    def timer_callback(self):


        self.x_error = self.x_goal - self.x
        self.y_error = self.y_goal - self.y

        if abs(self.x_error) > 0.5 and abs(self.y_error) > 0.5:
            self.p = math.sqrt(self.x_error**2 + self.y_error**2)
            self.alpha = math.atan2(self.y_error,self.x_error) - (self.theta)

            self.msg_controle.linear.x = self.v_max * math.tanh(self.p)
            self.msg_controle.angular.z = self.k_w * self.alpha
            self.publisher.publish(self.msg_controle)

        else:
            self.msg_controle.linear.x = 0.0
            self.msg_controle.angular.z = 0.0



def main(args=None):
    rclpy.init(args=args)

    controle = controler()

    rclpy.spin(controle)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controle.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

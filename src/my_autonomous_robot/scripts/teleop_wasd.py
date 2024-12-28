#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import termios
import tty

def get_key():
    """Klavyeden tek karakterlik giriş al."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def teleop():
    """WASD ile robot kontrolü."""
    rospy.init_node('teleop_wasd', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)  # 10 Hz
    print("""
    Kontrol Tuşları:
    ---------------------------
        W : İleri
        S : Geri
        A : Sola Dön
        D : Sağa Dön
        Q : Dur
    Çıkmak için CTRL+C'ye basın.
    """)

    twist = Twist()
    while not rospy.is_shutdown():
        key = get_key().lower()
        if key == 'w':
            twist.linear.x = 0.5  # İleri
            twist.angular.z = 0.0
        elif key == 's':
            twist.linear.x = -0.5  # Geri
            twist.angular.z = 0.0
        elif key == 'a':
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # Sola dön
        elif key == 'd':
            twist.linear.x = 0.0
            twist.angular.z = -0.5  # Sağa dön
        elif key == 'q':
            twist.linear.x = 0.0
            twist.angular.z = 0.0  # Dur
        else:
            print("Geçersiz tuş! Lütfen W, A, S, D veya Q tuşlarını kullanın.")

        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        teleop()
    except rospy.ROSInterruptException:
        pass


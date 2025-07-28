import cv2

cap = cv2.VideoCapture(0)

status, photo = cap.read()

print(status)

cv2.imshow("hi", photo)
cv2.waitKey(30000)
cv2.destroyAllWindows()

from cvzone.HandTrackingModule import HandDetector

brain_hand_detector = HandDetector()

my_hand_detector = brain_hand_detector.findHands(photo)

my_hand_lmlist = my_hand_detector[0][0]

my_finger_up = brain_hand_detector.fingersUp(my_hand_lmlist)

import boto3

if my_finger_up == [1, 1, 1, 1, 1]:
    ec2 = boto3.resource('ec2', region_name='ap-south-1')

    instances = ec2.create_instances(
        ImageId='ami-0d0ad8bb301edb745',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1
    )

    instance = instances[0]
    print(f"EC2 instance launched: {instance.id}")
else:
    print("Condition not met.")
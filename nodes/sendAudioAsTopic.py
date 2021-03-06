#!/usr/bin/python

import os
from time import sleep

import pyaudio

import rospkg
import rospy

from std_msgs.msg import String


# Class to publish audio to topic
class AudioMessage(object):

    def __init__(self):

        # Initializing publisher with buffer size of 10 messages
        self.pub_ = rospy.Publisher("sphinx_audio", String, queue_size=10)

        # initialize node
        rospy.init_node("audio_control")
        # Call custom function on node shutdown
        rospy.on_shutdown(self.shutdown)

        # All set. Publish to topic
        self.transfer_audio_msg()

    # Function to publish input audio to topic
    def transfer_audio_msg(self):

        rospy.loginfo("audio input node will start after delay of 5 seconds")
        sleep(5)

        # Initializing rospack to find package location
        rospack = rospkg.RosPack()

        # Params
        self._input = "~input"
        # Location of external files
        self.location = rospack.get_path('pocketsphinx') + '/demo/'

        # Checking if audio file given or system microphone is needed
        if rospy.has_param(self._input):
            if rospy.get_param(self._input) != ":default":
                stream = open(os.path.join(self.location +
                                           rospy.get_param(self._input)), 'rb')
            else:
                # Initializing pyaudio for input from system microhpone
                stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1,
                                                rate=16000, input=True, frames_per_buffer=1024)
                stream.start_stream()

        while not rospy.is_shutdown():
            buf = stream.read(1024)
            if buf:
                # Publish audio to topic
                self.pub_.publish(buf)
            else:
                break
        # mark end of audio
        self.pub_.publish("ended")

    def shutdown(self):
        # command executed after Ctrl+C is pressed
        rospy.loginfo("Stop ASRControl")
        rospy.sleep(1)


if __name__ == "__main__":
    AudioMessage()

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyNiRecorder
~~~~~~~~~~~~

This script implements a ONI file writer.


Usage: python2 PyNiRecorder

You should link the libOpenNI2.so and the OpenNI2 directory in the script path.
If they are located inside /usr/lib, you could

$ ln -s /usr/lib/libOpenNI2.so
$ > ln -s /usr/lib/OpenNI2

:copyright: (c) 2015 by Daniele Liciotti.
:license: Apache2, see LICENSE for more details.
:date: 2015-04-15
"""

import os, time
from primesense import openni2
from primesense import _openni2 as c_api
import cv2


def write_files(dev):
        """
        Captures the point cloud and write it on a Oni file. 
        """
        
        depth_stream = dev.create_depth_stream()
        color_stream = dev.create_color_stream()
        #ir_stream = dev.create_ir_stream()
        print (dev.get_sensor_info(openni2.SENSOR_DEPTH))

        depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 320, resolutionY = 240, fps = 30))
        color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 320, resolutionY = 240, fps = 30))
        depth_stream.start()
        color_stream.start()

        rec = openni2.Recorder(time.strftime("%Y%m%d%H%M")+".oni")
        rec.attach(depth_stream)
        rec.attach(color_stream)
        print (rec.start())
        raw_input("Press enter to terminate the recording")
        rec.stop()
        depth_stream.stop()
        color_stream.stop()

def main():
        """The entry point"""
        try:
            openni2.initialize()     # can also accept the path of the OpenNI redistribution
        except:
            print ("Device not initialized")
            return
        
        try:
            dev = openni2.Device.open_any()
            write_files(dev)
        except:
            print ("Unable to open the device")
            
        openni2.unload()

if __name__ == '__main__':
        main()

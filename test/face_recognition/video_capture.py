#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/20/18 7:35 AM
# @Author  : hys
# @Site    : 
# @File    : video_capture.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com

import cv2
import numpy as np
import face_recognition


class VideoCapture:
    """摄像头"""
    def __init__(self):
        """初始化摄像头"""
        # 获得一个cv2实力
        self.video_capture_cv2 = cv2
        # 打开笔记本内置摄像头
        self.video_capture = self.video_capture_cv2.VideoCapture(0)
        # 摄像头读取的帧
        self.frame = np.array([])
        # 屏幕上要显示的帧
        self.dis_frame = np.array([])
        # 通过摄像头获取的face_encodings
        self.face_encodings = []
        # 显示图像时检测到的键盘值
        self.keyboard = ""
        # 拍摄到的人脸特征信息
        self.face_locations = []

    def read_frame(self):
        """按帧读取拍摄到的内容"""
        # 读取内容
        ret, self.frame = self.video_capture.read()
        # 获得要在屏幕上显示的内容
        self.dis_frame = self.video_capture_cv2.resize(self.frame, (0, 0), fx=1.5, fy=1.5)

    def get_face_encodings(self):
        """获取当前拍摄到的人脸初级特征信息和face_encoding"""
        # 获取当前的frame
        self.read_frame()
        # 提取图片的特征信息
        small_frame = self.video_capture_cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        # 把图片调整到适合face_recognition的颜色格式
        rgb_small_frame = small_frame[:, :, ::-1]
        # 获取人脸特征信息
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        # 通过摄像头获得的人脸face_encodings
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        # 如果没有得到face_encoding继续扫描
        # if len(self.face_encodings) == 0:
        #     self.get_face_encoding()
        return self.face_encodings

    def mark_face(self):
        """标记人脸"""
        for (top, right, bottom, left) in self.face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            # 设置边框大小及位置
            top *= 6
            right *= 6
            bottom *= 6
            left *= 6

            # Draw a box around the face
            # 围绕脸部画一个方框
            self.video_capture_cv2.rectangle(self.dis_frame, (left, top), (right, bottom), (205, 0, 0), 2)

            # Draw a label with a name below the face
            # 在上面的方框下再画一个长方形，并写入名字
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(big_frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

    def display_frame(self):
        """把当前拍摄到的内容显示在屏幕上"""
        self.video_capture_cv2.imshow("hello world", self.dis_frame)
        self.keyboard = self.video_capture_cv2.waitKey(1) & 0xFF

    def destroy_instance(self):
        """销毁实例"""
        self.video_capture.release()
        self.video_capture_cv2.destroyAllWindows()


if __name__ == "__main__":
    print("vide_capture.py模块调试")
    vc = VideoCapture()
    # vc.get_face_encoding()
    # print(len(vc.face_encodings))
    # print(vc.face_encodings)
    while True:
        # vc.read_frame()
        vc.get_face_encodings()
        vc.mark_face()
        vc.display_frame()
        if vc.keyboard == ord("q"):
            vc.destroy_instance()
            break

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/7/18 11:01 PM
# @Author  : hys
# @Site    : 
# @File    : rel_time_face_recognition.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com

import face_recognition
import cv2

# 初始化本机摄像头
video_capture = cv2.VideoCapture(0)
# 库中图片
obama_img = face_recognition.load_image_file("image/pics_i_know/hys.jpg")
# 获取图片编码
obama_face_encoding = face_recognition.face_encodings(obama_img)[0]
# 声明location列表
face_locations = []
# 声明encoding列表
face_encodings = []
# 声明名称列表
face_names = []
# 声明标识位
process_this_frame = True

while True:
    # 读取摄像头拍摄到的内容
    ret, frame = video_capture.read()
    # 设置显示框大小、位置
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # 如果标识位为True
    if process_this_frame:
        # 生成face_locations
        face_locations = face_recognition.face_locations(small_frame)
        # 获取拍摄人物encoding
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 把拍摄到的face与已知的人物进行比较
            match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
            # 如果匹配
            if match[0]:
                name = "hys"
            else:
                name = "unknow"

            # 把识别出的人物名称保存到列表中
            face_names.append(name)
    # 取反
    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),  2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
        # 设置显示框的字体
        font = cv2.FONT_HERSHEY_DUPLEX
        # 把拍摄到的内容及识别出的名字显示到屏幕上
        cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


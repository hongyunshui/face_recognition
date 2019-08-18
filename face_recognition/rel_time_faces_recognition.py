#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/8/18 12:48 PM
# @Author  : hys
# @Site    : 
# @File    : rel_time_faces_recognition.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com

import os
import face_recognition
import cv2


class RelRecognition:
    """实时识别人脸"""
    def __init__(self):
        """初始化类中的属性"""

    @staticmethod
    def get_pic_path_and_names(file_path):
        """得到特定目录下所有的图片路径以及对应的图片名称"""
        # 声明人名及对应的文件路径字典
        picture_path_and_face_names = {}
        # 获取目录下所有文件的全名放入列表
        file_full_name_list = os.listdir(file_path)
        # 遍历文件获得图片路径和对应的人名
        for all_dir in file_full_name_list:
            # 获得完整文件路径
            children = os.path.join(file_path, all_dir)
            # 打开文件
            f = open(children)
            # print(children)
            # 获得文件全称
            base_name = os.path.basename(f.name)
            # 获取人名
            file_name = os.path.splitext(base_name)
            # 把文件路径和人名对应存储到列表
            picture_path_and_face_names[children] = file_name[0]
            # print(file_name[0])
            f.close()
        print("get_pic_path_and_names")
        return picture_path_and_face_names

    def get_names_and_encoding(self, file_path):
        """获取人名encoding"""
        names_and_encoding = {}
        pic_path_and_names = self.get_pic_path_and_names(file_path)
        for path, name in pic_path_and_names.items():
            # 读取图片信息
            image = face_recognition.load_image_file(path)
            # 获得图片encoding
            face_encoding = face_recognition.face_encodings(image)[0]
            names_and_encoding[name] = face_encoding
        print("get_names_and_encoding")
        return names_and_encoding

    def rel_time_recognition(self, file_path):
        """实时识别"""
        # 初始化本机摄像头
        video_capture = cv2.VideoCapture(0)
        # 声明location列表
        face_locations = []
        # 声明标识位
        process_this_frame = True
        # 声明名称列表
        face_names = []
        # 获取现有库中的人名和face_encoding
        old_names_and_encoding = self.get_names_and_encoding(file_path)
        for key in old_names_and_encoding:
            print(key)
        print(old_names_and_encoding)
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
                new_face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                for new_face_encoding in new_face_encodings:
                    face_names = []
                    rel_time_face_name = "unknow people"
                    for name, old_encoding in old_names_and_encoding.items():
                        print(name + "***")

                        match = face_recognition.compare_faces([old_encoding], new_face_encoding)
                        match[0] = False
                        if match:
                            rel_time_face_name = name
                            break
                    # 把识别出的名字保存到列表中
                    face_names.append(rel_time_face_name)
            # 取反
            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
                # 设置显示框的字体
                font = cv2.FONT_HERSHEY_DUPLEX
                # 把拍摄到的内容及识别出的名字显示到屏幕上
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__name__)
    filePath = "image/pics_i_know"
    rtr = RelRecognition()
    rtr.rel_time_recognition(filePath)

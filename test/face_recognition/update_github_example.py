#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/18/18 5:47 PM
# @Author  : hys
# @Site    : 
# @File    : update_github_example.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com
import face_recognition
import cv2
import numpy as np
# import json
import csv
import datetime
import os


class UGE:
    """升级版多人脸识别"""
    def __init__(self):
        """初始化UGE"""
        # Get a reference to webcam #0 (the default one)
        # self.video_capture = cv2.VideoCapture(0)
        self.face_locations = []
        self.process_this_frame = True
        # 声明一些变量
        self.face_names = []
        # 运行模式标识位 1：增加人员  2：打卡  3：选择运行模式
        self.model_flag = 3
        # 密码
        self.pwd = False
        #
        self.known_face_names = []
        #
        self.known_face_encodings = []
        # 打卡类型 0：早上上班打卡    1：晚上下班打卡
        self.sign_in_model = 1
        # 是否迟到早退标识位 1:是  0：否
        self.exp_flag = 1

    @staticmethod
    def make_face_encodings():
        """生成face_encodings并存储到磁盘"""
        # Load a sample picture and learn how to recognize it.
        lipanpan_image = face_recognition.load_image_file("../image/pics_i_know/lipanpan.jpg")
        lipanpan_face_encoding = face_recognition.face_encodings(lipanpan_image)[0]
        np.save(file="lipanpan.npy", arr=lipanpan_face_encoding)

        # Load a second sample picture and learn how to recognize it.
        hys_image = face_recognition.load_image_file("../image/pics_i_know/hys.jpg")
        hys_face_encoding = face_recognition.face_encodings(hys_image)[0]
        np.save(file="hys.npy", arr=hys_face_encoding)

    @staticmethod
    def get_arr_path_and_names():
        """得到特定目录下所有的图片路径以及对应的图片名称"""
        file_path = "../face_encodings"
        # 声明人名及对应的文件路径字典
        arr_path_and_face_names = {}
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
            arr_path_and_face_names[children] = file_name[0]
            # print(file_name[0])
            f.close()
        return arr_path_and_face_names

    def get_face_encodings(self):
        """从磁盘获取face_encodings"""
        arr_path_and_face_names = self.get_arr_path_and_names()
        for arr_path, face_n in arr_path_and_face_names.items():
            face_encoding = np.load(file=arr_path)
            self.known_face_names.append(face_n)
            self.known_face_encodings.append(face_encoding)
        # return self.know_face_encodings

    @staticmethod
    def current_face_encodings():
        """调用摄像头获取当前拍摄到的所有人脸的face_encodign"""
        # 打开笔记本内置摄像头
        video_capture = cv2.VideoCapture(0)
        # 按帧读取视频
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # 把图片色彩从BGR格式转变为RGB格式以供face_recognition使用
        rgb_small_frame = small_frame[:, :, ::-1]
        # 识别出当前摄像头拍摄到的所有的人脸，并生成face_encoding
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        return face_encodings

    def record_sign_in(self, name):
        """记录考勤情况"""
        now_time = datetime.datetime.now()
        now_day = now_time.strftime("%Y-%m-%d")
        now_hour = now_time.strftime("%H:%M:%S")

        # row1 = ["名称", "打卡类型", "时间", "是否迟到或早退", "日期"]
        row2 = [name, self.sign_in_model, now_hour, self.exp_flag, now_day]
        out = open("sign_in.csv", "a", newline="")
        csv_writer = csv.writer(out, dialect="excel")
        csv_writer.writerow(row2)
        self.exp_flag = 1

    @staticmethod
    def if_sign_in_time(self):
        """判断是否在打卡时间"""
        now_time = datetime.datetime.now()
        now_day = now_time.strftime("%Y-%m-%d")
        print(type(now_time))
        # 开始签到时间 字符
        sig_in_star_hour = "07:30:00"
        sish = now_day + " " + sig_in_star_hour
        sig_in_star_time = datetime.datetime.strptime(sish, "%Y-%m-%d %H:%M:%S")

        # 结束签到时间 字符
        sig_in_end_hour = "08:30:00"
        sieh = now_day + " " + sig_in_end_hour
        sig_in_end_time = datetime.datetime.strptime(sieh, "%Y-%m-%d %H:%M:%S")

        # 下班开始签到时间
        after_work_star_hour = "18:00:00"
        awsh = now_day + " " + after_work_star_hour
        after_work_star_time = datetime.datetime.strptime(awsh, "%Y-%m-%d %H:%M:%S")
        after_work_end_hour = "19:00:00"
        aweh = now_day + " " + after_work_end_hour
        after_work_end_time = datetime.datetime.strptime(aweh, "%Y-%m-%d %H:%M:%S")

        # 是否在上班打卡时间，如果是就返回True
        if (now_time > sig_in_star_time) and (now_time < sig_in_end_time):
            print("开始")
            self.sign_in_model = 0
            self.exp_flag = 0
            return True
        # 是否在下班打卡时间，如果是就返回True
        elif (now_time > after_work_star_time) and (now_time < after_work_end_time):
            self.sign_in_model = 1
            self.exp_flag = 0
            print("下班")
            return True
        else:
            return False

    @staticmethod
    def display_face(self, face_names, big_frame):
        """在屏幕上显示结果"""
        # Display the results
        # 设置方框大小和位置
        for (top, right, bottom, left), name in zip(self.face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            # 设置边框大小及位置
            top *= 6
            right *= 6
            bottom *= 6
            left *= 6

            # Draw a box around the face
            # 围绕脸部画一个方框
            cv2.rectangle(big_frame, (left, top), (right, bottom), (205, 0, 0), 2)

            # Draw a label with a name below the face
            # 在上面的方框下再画一个长方形，并写入名字
            cv2.rectangle(big_frame, (left, bottom - 35), (right, bottom), (255, 245, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(big_frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        # Display the resulting image
        cv2.imshow('Look Your Face', big_frame)

    @staticmethod
    def sign_in(self, known_face_names, rgb_small_frame, known_face_encodings):
        """打卡"""

        # 识别出当前摄像头拍摄到的所有的人脸，并生成face_encoding
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        print(type(self.face_locations))
        face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        print(len(face_encodings))
        face_names = []
        for face_encoding in face_encodings:
            # 识别拍摄到的人脸是否在已知的人脸中
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # 如果人脸匹配
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                # 当只拍摄到一个人脸且被识别出时更新face_encoding
                if len(face_encodings) == 1:
                    file_path = "../face_encodings/" + name + ".np"
                    np.save(file=file_path, arr=face_encoding)
                    # self.model_flag = 3
                    self.record_sign_in(name)
                # print(file_name)
            face_names.append(name)

        return face_names

    def run_sign_in(self, rgb_small_frame):
        """考勤主函数"""
        self.face_names = []
        if self.process_this_frame:
            if not self.if_sign_in_time(self):
                print("可以打卡")
                self.face_names = self.sign_in(self, self.known_face_names, rgb_small_frame, self.known_face_encodings)
            else:
                print("非打卡时间")
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_names = ["time is wrong"]
        self.process_this_frame = not self.process_this_frame

    @staticmethod
    def increase_face(self, rgb_small_frame):
        """增加人脸"""
        print("增加人脸")
        # 识别出当前摄像头拍摄到的所有的人脸，并生成face_encoding
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        self.face_names = "Enter Your Name"
        if len(face_encodings) == 1:
            your_name = input("Enter Your Name:")
            file_path = "../face_encodings/" + your_name + ".npy"
            print(file_path)
            np.save(file=file_path, arr=face_encodings[0])
            self.model_flag = 3
            self.get_face_encodings()
            print(your_name)

    def set_run_model(self, rgb_small_frame):
        """打开后选择运行方式"""
        print("选择运行方式")
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        # 如果密码标识位为True,则进入模式设置状态
        k = cv2.waitKey(1) & 0xFF
        if self.pwd:
            self.face_names = [" mode: 1 2 3 "]
            if k == ord('2'):
                self.model_flag = 2
            elif k == ord('1'):
                self.model_flag = 1
        else:
            self.face_names = ["Enter Password"]
        # 如果密码正确则将标识位置为True
        if k == ord("a"):
            self.pwd = True

    def main(self):
        """主函数"""
        # 打开笔记本内置摄像头
        video_capture = cv2.VideoCapture(0)
        # 获取已知的人脸face_encodings
        # known_face_encodings = self.get_face_encodings()
        self.get_face_encodings()
        # 获取已知的姓名
        # known_face_names = self.known_face_names

        while True:
            # Grab a single frame of video
            # 按帧读取视频
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            big_frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # self.face_locations = face_recognition.face_locations(rgb_small_frame)

            if self.model_flag == 1:
                self.increase_face(self, rgb_small_frame)
            elif self.model_flag == 2:
                self.run_sign_in(rgb_small_frame)
            elif self.model_flag == 3:
                self.set_run_model(rgb_small_frame)

            # 在屏幕上显示结果
            self.display_face(self, self.face_names, big_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release handle to the webcam
        # 释放对象销毁窗口
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fa_re = UGE()
    fa_re.main()


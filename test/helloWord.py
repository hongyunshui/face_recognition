import face_recognition

pic_of_me = face_recognition.load_image_file("image/pics_i_know/hong.jpg")
my_face_encoding = face_recognition.face_encodings(pic_of_me)[0]
print(my_face_encoding)
unknown_pic = face_recognition.load_image_file("image/pics_unknow/hg.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_pic)[0]
print(unknown_encoding)
results = face_recognition.compare_faces([my_face_encoding], unknown_encoding)
print(results[0])
if results[0] == True:
    print("it's me")
else:
    print("not me")





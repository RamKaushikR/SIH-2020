import numpy as np
import os
import pickle
import face_recognition
import warnings
import time
import cv2


warnings.filterwarnings('ignore')


class Face_Identify:
    """
    Creates an identify object, to identify a face from an image
    Parameters:
    :source: The source path for the image files, default identify/
    :models: The file where the face models are stored, default face_models.dat
    """
    def __init__(self, source = 'identify/', models = 'face_models.dat'):
        self.source = source
        self.face_model = pickle.load(open(models, 'rb'))
        self.models = np.array(list(self.face_model.values()))
        self.faces = list(self.face_model.keys())
        
    def identify_face(self, name):
        """
        Identifies a given face from an image
        """
        try:
            files = os.listdir(self.source)

            for file in files:
                print(file)
                count = 0
                found = False

                """
                img = cv2.imread(self.source + file)
                img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(self.source + file, img)
                """

                file_image = face_recognition.load_image_file(self.source + file)
                file_encoding = face_recognition.face_encodings(file_image)[0]

                for i in range(len(self.models)):
                    face_encodings = self.models[i]
                    result = face_recognition.compare_faces([file_encoding], face_encodings)

                    if result[0]:
                        found = True
                        break

                    count += 1

                os.remove(self.source + file)
                if count == len(self.models):
                    face = 'Unidentified'
                else:
                    face = self.faces[count]
                print(face)

                if found and face == name:
                    return 1
                return 0

        except:
            return -1


if __name__ == '__main__':
    face = Face_Identify()
    face.identify_face()

import sys
import os
import pickle
import face_recognition
import warnings
import cv2


warnings.filterwarnings('ignore')


class Face:
    """
    Creates a face object, to add and update face models
    Parameters:
    :source: The source path for the picture files, default faces
    :models: The file where the face models are stored, default face_models.dat
    """
    def __init__(self, source = 'faces/', models = 'face_models.dat'):
        self.source = source
        self.models = models
            
    def add_face(self, name):
        """
        Adds a new face model
        Parameters:
        :name: The name of the person
        """
        try:
            files = os.listdir(self.source)[0]
            """
            img = cv2.imread(self.source + files)
            img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(self.source + files, img)
            """

            image = face_recognition.load_image_file(self.source + files)
            image_encodings = face_recognition.face_encodings(image)[0]

            if self.models in os.listdir('./'):
                model = pickle.load(open(self.models, 'rb'))
            else:
                model = {}

            model[name] = image_encodings
            pickle.dump(model, open(self.models, 'wb'))

            os.remove(self.source + files)
            return 'Added ' + name

        except:
            return 'Could not add ' + name
            
    def update_face(self, name):
        """
        Updates an existing face model
        Parameters:
        :name: The name of the person
        """
        try:
            files = os.listdir(self.source)[0]
    
            image = face_recognition.load_image_file(self.source + files)
            image_encodings = face_recognition.face_encodings(image)[0]
        
            model = pickle.load(open(self.models, 'rb'))
            model[name] = image_encodings

            pickle.dump(model, open(self.models, 'wb'))

            os.remove(self.source + files)
            return 'Updated ' + name

        except:
            return 'Could not identify ' + name

    def remove_face(self, name):
        """
        Removes an existing face model
        Parameters:
        :name: The name of the person
        """
        try:
            model = pickle.load(open(self.models, 'rb'))
            _ = model.pop(name)

            if len(model.keys()) == 0:
                os.remove(self.models)
            else:
                pickle.dump(model, open(self.models, 'wb'))
            return 'Removed ' + name

        except:
            return 'Could not remove ' + name


if __name__ == '__main__':
    face = Face()
    choice = int(sys.argv[2])
    
    if choice == 1:
        face.add_face(sys.argv[1])
    elif choice == 2:
        face.update_face(sys.argv[1])
    else:
        face.remove_face(sys.argv[1])

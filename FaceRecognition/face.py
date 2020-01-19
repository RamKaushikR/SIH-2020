import sys
import os
import pickle
import face_recognition
import warnings


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
        files = os.listdir(self.source)[0]
        
        image = face_recognition.load_image_file(self.source + files)
        image_encodings = face_recognition.face_encodings(image)[0]

        if self.models in os.listdir('./'):
            model = pickle.load(open(self.models, 'rb'))
        else:
            model = {}

        model[name] = image_encodings
        pickle.dump(model, open(self.models, 'wb'))
        print('Model developed for ' + name)

        os.remove(self.source + files)
            
    def update_face(self, name):
        """
        Updates an existing face model
        Parameters:
        :name: The name of the person
        """
        files = os.listdir(self.source)[0]
        
        image = face_recognition.load_image_file(self.source + files)
        image_encodings = face_recognition.face_encodings(image)[0]
                
        model = pickle.load(open(self.models, 'rb'))
        model[name] = image_encodings
        
        pickle.dump(model, open(self.models, 'wb'))
        print('Model updated for ' + name)

        os.remove(self.source + files)

    def remove_face(self, name):
        """
        Removes an existing face model
        Parameters:
        :name: The name of the person
        """
        model = pickle.load(open(self.models, 'rb'))
        _ = model.pop(name)

        print('Removed ' + name)

        pickle.dump(model, open(self.models, 'wb'))


if __name__ == '__main__':
    face = Face()
    choice = int(sys.argv[2])
    
    if choice == 1:
        face.add_face(sys.argv[1])
    elif choice == 2:
        face.update_face(sys.argv[1])
    else:
        face.remove_face(sys.argv[1])

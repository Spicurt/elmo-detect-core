from multiprocessing import Process

def sound():
    import soundPy

def FaceDetect():
    import faceDetect

if __name__ == '__main__':
    Process(target=sound).start()
    Process(target=FaceDetect).start()
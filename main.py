from multiprocessing import Process

def mainProcess():
    import pictureTake

if __name__ == '__main__':
    Main = Process(target = mainProcess)
    Main.start()
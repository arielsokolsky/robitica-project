import cv2
import mediapipe as mp
from dataclasses import dataclass, field
from threading import Thread


MY_CAM_PORT = 0
WINDOW_NAME = "Win"
WINDOW_CLOSED = 0
all_threads = []

def main():
    close_windows()
    cam1 = cam_manager(WINDOW_NAME + "1", MY_CAM_PORT)
    #cam2 = cam_manager(WINDOW_NAME + "2", MY_CAM_PORT)

    cam1.screen_display(False)
    #cam2.screen_display(True)

    for thread in all_threads:
        thread.join()
    return 0


@dataclass
class cam_manager():
    name : str
    port : int
    cap : None = None
    img : None = None
    thread : None = None
    hands : None = None
    hands_mp : None = None
    hands_coord : None = None
    hands_draw : None =  None

    def __post_init__(self):
        self.cap = cv2.VideoCapture(self.port)
        self.hands_mp = mp.solutions.hands
        self.hands = self.hands_mp.Hands()
        self.hands_draw = mp.solutions.drawing_utils

    #get the picture from cap
    def __get_picture(self):
        success, self.img = self.cap.read()
        return success

    #create window and display img
    def __show_picture(self):
        cv2.imshow(self.name, self.img)
        cv2.waitKey(1)


    def __get_hands(self):
        #convert the picture to rgb and process
        imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(imgRGB)
        self.hands_coord = result.multi_hand_landmarks

        if self.hands_coord:
            for hand in self.hands_coord:
                self.hands_draw.draw_landmarks(self.img, hand, self.hands_mp.HAND_CONNECTIONS)


    #take the img from the screen and display the the cam in a new window
    def __display_screen_forever(self, with_hands):
        #create the window
        self.__get_picture()
        self.__show_picture()

        while cv2.getWindowProperty(self.name, 0) >= WINDOW_CLOSED:
            self.__get_picture()
            if with_hands:
                self.__get_hands()
            self.__show_picture()

    def __get__point__coord(self):
        print("5")
        #for id, lm in enumerate(self.hands_lms)

    def screen_display(self, with_hands):
        self.thread = Thread(target = self.__display_screen_forever, args=(with_hands, ))
        self.thread.start()
        all_threads.extend([self.thread])


#get the name of the window and close it (if didn't get name close all windows)
def close_windows(name):
    if name == "":
        cv2.destroyAllWindows()
    else:
        cv2.destroyWindow(name)


if __name__ == '__main__':
    main()

import pyautogui
import numpy as np

class Controller:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_Landmarks = None
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    Thump_finger_down = None 
    Thump_finger_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_Thumb_finger = None
    middle_finger_within_Thumb_finger = None
    little_finger_within_Thumb_finger = None
    ring_finger_within_Thumb_finger = None
    screen_width, screen_height = pyautogui.size()

    alpha = 0.2  
    smoothed_x = None
    smoothed_y = None

    @staticmethod
    def update_fingers_status():
        Controller.little_finger_down = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[17].y
        Controller.little_finger_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.index_finger_down = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[5].y
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.middle_finger_down = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[9].y
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[9].y
        Controller.ring_finger_down = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[13].y
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_down = Controller.hand_Landmarks.landmark[4].y > Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[13].y
        Controller.all_fingers_down = Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        Controller.all_fingers_up = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up
        Controller.index_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[2].y
        Controller.middle_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[2].y
        Controller.little_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[2].y
        Controller.ring_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[2].y

    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        if Controller.smoothed_x is None or Controller.smoothed_y is None:
            Controller.smoothed_x = current_x
            Controller.smoothed_y = current_y
        else:
            Controller.smoothed_x = Controller.alpha * current_x + (1 - Controller.alpha) * Controller.smoothed_x
            Controller.smoothed_y = Controller.alpha * current_y + (1 - Controller.alpha) * Controller.smoothed_y
        return int(Controller.smoothed_x), int(Controller.smoothed_y)


    @staticmethod
    def cursor_moving():
        if Controller.hand_Landmarks is not None:
            point = 9  
            current_x, current_y = Controller.hand_Landmarks.landmark[point].x, Controller.hand_Landmarks.landmark[point].y
            cursor_freezed = Controller.all_fingers_up and Controller.Thump_finger_down
            if not cursor_freezed:
                smoothed_x, smoothed_y = Controller.get_position(current_x, current_y)
                pyautogui.moveTo(smoothed_x, smoothed_y, duration=0)


    @staticmethod
    def detect_scrolling():
        scrolling_up = Controller.little_finger_up and Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down
        if scrolling_up:
            pyautogui.scroll(120)
            print("Scrolling UP")

        scrolling_down = Controller.index_finger_up and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        if scrolling_down:
            pyautogui.scroll(-120)
            print("Scrolling DOWN")

    @staticmethod
    def detect_clicking():
        left_click_condition = Controller.index_finger_within_Thumb_finger and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up and not Controller.middle_finger_within_Thumb_finger and not Controller.ring_finger_within_Thumb_finger and not Controller.little_finger_within_Thumb_finger
        if not Controller.left_clicked and left_click_condition:
            pyautogui.click()
            Controller.left_clicked = True
            print("Left Clicking")
        elif not Controller.index_finger_within_Thumb_finger:
            Controller.left_clicked = False
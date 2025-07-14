import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from PyQt5.QtCore import QThread

class ControllerThread(QThread):
    def __init__(self, sensitivity=5):
        super().__init__()
        self.running = True
        self.sensitivity = sensitivity

    def stop(self):
        self.running = False

    def run(self):
        cap = cv2.VideoCapture(0)
        screen_w, screen_h = pyautogui.size()
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                nose = landmarks[1]
                left_eye = landmarks[159]
                right_eye = landmarks[386]

                screen_x = screen_w * nose.x
                screen_y = screen_h * nose.y

                pyautogui.moveTo(screen_x, screen_y, duration=0.01)

                left_ratio = self._eye_aspect_ratio(landmarks, left=True)
                right_ratio = self._eye_aspect_ratio(landmarks, left=False)

                if left_ratio < 0.22 and right_ratio > 0.26:
                    pyautogui.click(button='left')
                elif right_ratio < 0.22 and left_ratio > 0.26:
                    pyautogui.click(button='right')

            cv2.waitKey(1)

        cap.release()

    def _eye_aspect_ratio(self, lm, left=True):
        if left:
            top = np.array([lm[159].x, lm[159].y])
            bottom = np.array([lm[145].x, lm[145].y])
            left = np.array([lm[33].x, lm[33].y])
            right = np.array([lm[133].x, lm[133].y])
        else:
            top = np.array([lm[386].x, lm[386].y])
            bottom = np.array([lm[374].x, lm[374].y])
            left = np.array([lm[362].x, lm[362].y])
            right = np.array([lm[263].x, lm[263].y])

        vertical = np.linalg.norm(top - bottom)
        horizontal = np.linalg.norm(left - right)
        ratio = vertical / horizontal
        return ratio

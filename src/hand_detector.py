import cv2
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import (
    DrawingSpec,
    draw_landmarks)


class HandDetector:
    def __init__(self,
                 static_image_mode=False,
                 max_hands=2,
                 detection_confiance=0.7,
                 tracking_confiance=0.6,
                 model_complexity=0,
                 points_color=(0, 0, 255),
                 lines_color=(255, 255, 255)):

        self.static_image_mode = static_image_mode
        self.max_hands = max_hands
        self.detection_confiance = detection_confiance
        self.tracking_confiance = tracking_confiance
        self.model_complexity = model_complexity
        self.lines_color = lines_color

        self.hands = Hands(
            self.static_image_mode,
            self.max_hands,
            self.model_complexity,
            self.detection_confiance,
            self.tracking_confiance
        )

        self.drawing_points_config = DrawingSpec(
            color=points_color
        )

        self.drawing_lines_config = DrawingSpec(
            color=self.lines_color
        )

    def find_hands(self,
                   image,
                   draw=True):

        # Por padrão, as imagens do OpenCV se encontram em
        # formato BGR, não RGB. Sendo assim, é necessário
        # converter para RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.result = self.hands.process(image_rgb)

        if self.result.multi_hand_landmarks is not None:  # type: ignore
            for points in self.result.multi_hand_landmarks:  # type: ignore
                if draw:
                    draw_landmarks(
                        image,
                        points,
                        HAND_CONNECTIONS,  # type: ignore
                        self.drawing_points_config,
                        self.drawing_lines_config
                    )
        return image

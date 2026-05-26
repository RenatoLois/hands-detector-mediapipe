# python version    -> 3.9.25
# OpenCv version    -> 4.13.0
# mediapipe version -> 0.10.14
# PyOpenGL version  -> 3.1.10
# glfw version      -> 2.10.0

# credits for HandDetector class inspiration:
# https://www.youtube.com/@Mundo_Python

import cv2
import OpenGL.GL as gl
from hand_detector import HandDetector
from window import Window


def main():
    # model complexity ->
    # 0 = (- qualidade, + desempenho)
    # 1 = (+ qualidade, - desempenho)
    detector = HandDetector(model_complexity=1)

    cap = cv2.VideoCapture(0)
    Window.initialize_glfw()
    window = Window("hands detector", 720, 480)

    _, image = cap.read()
    image_height = image.shape[0]
    image_width = image.shape[1]
    image_channels = image.shape[2]

    image_format = None

    if image_channels == 3:
        image_format = gl.GL_RGB
    elif image_channels == 4:
        image_format = gl.GL_RGBA
    else:
        raise RuntimeError("image channel format not recognized")

    # OpenCV tem origem superior-esquerda, OpenGL inferior-esquerda
    image = cv2.flip(image, -1)  # invertendo horizontalmente e verticalmente

    # gerando textura
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_WRAP_S,
                       gl.GL_REPEAT)

    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_WRAP_T,
                       gl.GL_REPEAT)

    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_MIN_FILTER,
                       gl.GL_LINEAR)

    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_MAG_FILTER,
                       gl.GL_LINEAR)

    gl.glTexImage2D(gl.GL_TEXTURE_2D,
                    0,
                    image_format,
                    image_width,
                    image_height,
                    0,
                    image_format,
                    gl.GL_UNSIGNED_BYTE,
                    image)

    window.visible(True)

    # main loop
    while True:
        window.poll_events()
        _, image = cap.read()
        image = cv2.flip(image, 1)
        image = detector.find_hands(image=image)
        cv2.imshow("capture", image)
        cv2.waitKey(1)
        window.swap_buffers()


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    exit(0)

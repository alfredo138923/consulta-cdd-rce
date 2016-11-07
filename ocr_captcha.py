import cv2
import os
from PIL import Image


def image_black_white(imagen_path):
    """
        Transforma una imagen a blanco y negro
    :param imagen_path:
    """
    col = Image.open(imagen_path)
    gray = col.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')

    bw.save(imagen_path)


def vaciar_temp_captcha():
    filelist = [f for f in os.listdir("temp_captcha")]
    for f in filelist:
        # if f != 'captcha.png':
        os.remove('temp_captcha/' + f)


def get_captcha_desde_imagen(imagen):
    im = cv2.imread(imagen)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        if cv2.contourArea(cnt) > 14000:
            [x, y, w, h] = cv2.boundingRect(cnt)

            if 70 <= h <= 75:
                file_name = "temp_captcha/captcha.png".format(x)
                rot_orig = im[y:y + h - 10, x:x + w - 10]
                rot_orig = cv2.resize(rot_orig, (150, 100))
                cv2.imwrite(file_name, rot_orig)


def extraer_digitos(imagen):
    im = cv2.imread(imagen)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    # ################ Encontrar contornos ###################

    contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    responses = []
    for cnt in contours:

        # Encontrar el contorno del rectangulo del captcha
        if cv2.contourArea(cnt) > 40:
            [x, y, w, h] = cv2.boundingRect(cnt)

            if h > 10:  # tamano del digito
                file_name = "temp_captcha/{0}.png".format(x)
                rot_orig = gray[y:y + h, x:x + w]
                rot_orig = cv2.resize(rot_orig, (28, 28))

                cv2.imwrite(file_name, rot_orig)
                image_black_white(file_name)

                responses.append(str(x) + '.png')

    return responses

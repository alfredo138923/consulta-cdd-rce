# -*- encoding: utf-8 -*-
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from neural_models import NeuralModel
from ocr_captcha import extraer_digitos, vaciar_temp_captcha, \
    get_captcha_desde_imagen

__author__ = 'Alfredo Marcillo'

def process_data(identificacion):
    vaciar_temp_captcha()

    driver = webdriver.Firefox() 
    #driver = webdriver.PhantomJS()
    neuronal_model = NeuralModel()
    # neuronal_model.entrenar_modelo()
    neuronal_model.restaurar_modelo()


    print 'esperando rce...'
    driver.get("https://servicios.registrocivil.gob.ec/cdd/")

    tab_busq_cedula = driver.find_element_by_id(
        "__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1")

    tab_busq_cedula.click()

    inputCDD = driver.find_element_by_id(
        "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_TextBoxCedula")
    inputCDD.clear()
    inputCDD.send_keys(identificacion)

    inputCaptcha = driver.find_element_by_id(
        "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_txtVerificaCaptcha")
    inputCaptcha.click()

    driver.save_screenshot('temp_captcha/screenshot.png')
    print 'Guardando captcha.png...'
    get_captcha_desde_imagen('temp_captcha/screenshot.png')

    print 'extrayendo digitos...'
    imagen_digitos = extraer_digitos('temp_captcha/captcha.png')

    imagen_digitos_tmp = [int(x.split('.')[0]) for x in imagen_digitos]

    captcha_digitos = ''
    for img_item in sorted(imagen_digitos_tmp):
        img = 'temp_captcha/{0}.png'.format(img_item)
        prediccion = neuronal_model.clasificar_imagen(img)
        captcha_digitos += str(prediccion)

    print 'Prediccion de la red neuronal: ', captcha_digitos

    # Enviar prediccion al RC
    inputCaptcha.send_keys(captcha_digitos)

    inputCaptcha = driver.find_element_by_id(
            "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_ButtonConsultar")
    inputCaptcha.click()
        
    try:
        cedula_cedulado = driver.find_element_by_id(
            "ctl00_ContentPlaceHolder1_LabelCédula")
        nombre_cedulado = driver.find_element_by_id(
            "ctl00_ContentPlaceHolder1_LabelNombre")
        condicion_cedulado = driver.find_element_by_id(
                "ctl00_ContentPlaceHolder1_LabelCondiciónCedulado")
    except NoSuchElementException as ex:
        print '======= fallo al resolver captcha o cedula incorrecta========'
        
    else:
        print 'Cedula cedulado: ', cedula_cedulado.text
        print 'Nombre cedulado: ', nombre_cedulado.text
        print 'Condicion cedulado: ', condicion_cedulado.text

    # liberar recursos
    driver.quit()


if __name__ == '__main__':
    try:
        cedula = sys.argv[1]
    except IndexError as ex:
        print('Debes especificar la cedula como argumento')
    else:
        process_data(cedula)

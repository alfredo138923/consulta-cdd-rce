## Consulta cedula Ecuador
------------
Mediante el uso de la librería para machine learning TensorFlow se creó un modelo el cual da un predicción 
de los números del captcha de la pagina del RC y envía el resultado devuelta para obtener los datos del ciudadano.

Para entrenar el modelo se usó alrededor de 200 images por cada digito.

La precision del modelo es aproximadamente 94% por cada digito del captcha.

### Pre requisitos:
> Python2.7

> OpenCV

### Instrucciones:
Instalar opencv:
> aptitude install python-opencv
  
Crear un virtualenv y activarlo:
> virtualenv --system-site-packages ve 

> source ve/bin/activate

Instalar paquetes pip:
> pip install -r requerimientos.txt

Ejecutar script:
> python cdd-resolver.py 100xxx06x4

------------
## Contacto

E-mail: alfredo138923@openmailbox.org

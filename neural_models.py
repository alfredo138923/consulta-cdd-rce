import cv2
import numpy as np
import tensorflow as tf
import input_data


class NeuralModel:
    def __init__(self):
        self.sess = tf.Session()
        self.x = tf.placeholder("float", [None, 784])
        W = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))

        self.y = tf.nn.softmax(tf.matmul(self.x, W) + b)
        self.saver = tf.train.Saver()  # Guardar todas las variables

    def entrenar_modelo(self):
        mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
        y_ = tf.placeholder("float", [None, 10])

        cross_entropy = -tf.reduce_sum(y_ * tf.log(self.y))

        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(
                cross_entropy
        )

        init = tf.initialize_all_variables()

        self.sess.run(init)

        # Entrenar modelo
        iterador = 2000
        for i in range(iterador):
            batch_xs, batch_ys = mnist.train.next_batch(10)
            self.sess.run(
                    train_step, feed_dict={self.x: batch_xs, y_: batch_ys}
            )

        # Evaluar modelo:
        correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(y_, 1))

        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print "Precision %100: ", self.sess.run(
                accuracy,
                feed_dict={self.x: mnist.test.images, y_: mnist.test.labels}
        ) * 100

        self.saver.save(self.sess, 'data/model.ckpt')

    def restaurar_modelo(self):
        self.saver.restore(self.sess, 'data/model.ckpt')

    def clasificar_imagen(self, imagen):
        """
        Using our model to classify MNIST digit from a custom image:
        :param imagen:
        :return: Prediccion del digito en la imagen
        """

        # Fuente http://stackoverflow.com/a/34054866

        # Crear un array donde guardar la imagen
        images = np.zeros((1, 784))

        # read the image
        gray = cv2.imread(imagen, 0)

        """
        all images in the training set have an range from 0-1
        and not from 0-255 so we divide our flatten images
        (a one dimensional vector with our 784 pixels)
        to use the same 0-1 based range
        """
        flatten = gray.flatten() / 255.0
        """
        we need to store the flatten image and generate
        the correct_vals array
        correct_val for a digit (9) would be
        [0,0,0,0,0,0,0,0,0,1]
        """
        images[0] = flatten

        my_classification = self.sess.run(
                tf.argmax(self.y, 1), feed_dict={self.x: [images[0]]}
        )

        """
        we want to run the prediction and the accuracy function
        using our generated arrays (images and correct_vals)
        """
        return my_classification[0]

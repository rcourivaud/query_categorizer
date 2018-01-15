from keras.layers import InputLayer, Dense, Dropout
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.models import load_model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np

from query_categorizer.models.embedding_model import EmbeddingModel


class BaggingModel(object):
    def __init__(self, path_to_embedding_model, encoder):
        """

        :param path_to_embedding_model:
        :param encoder:
        """
        self.em = EmbeddingModel(path_to_embedding_model)
        self.encoder = encoder

    @staticmethod
    def create_model(input_shape, layers=None):
        """

        :param input_shape:
        :param layers:
        :return:
        """

        if layers is None:
            layers = [
                InputLayer(input_shape=(input_shape,)),
                Dense(100, activation='relu'),
                Dropout(0.1),
                Dense(200, activation='relu'),
                Dropout(0.1),
                Dense(200, activation='relu'),
                Dropout(0.1),
                Dense(9, activation='softmax')
            ]
        model = Sequential(layers=layers)
        model.compile(optimizer='adam', loss='categorical_crossentropy')

        return model

    @staticmethod
    def fit_model(model, X, y, test_size=None, save_path=None, tensorboard_log_path=None):
        """

        :param model:
        :param X:
        :param y:
        :param test_size:
        :param save_path:
        :param tensorboard_log_path:
        :return:
        """

        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size)
        callbacks = [TensorBoard(log_dir="./log/bagging/", ), ] if tensorboard_log_path else []

        model.fit(x=x_train,
                  y=y_train,
                  validation_data=(x_test,
                                   y_test,),
                  callbacks=callbacks,
                  epochs=10)

        if save_path is not None:
            model.save(save_path)

    @staticmethod
    def load_bagging_model(path_to_model):
        """

        :param path_to_model:
        :return:
        """
        return load_model(filepath=path_to_model)

    def get_train_data(self, texts, labels, web_results, test_split=False):
        """

        :param texts:
        :param labels:
        :param web_results:
        :param test_split:
        :return:
        """

        l_of_vectors = []
        l_of_labels = []

        for text, label, web_res in zip(texts, labels, web_results):
            all_vector = [self.em.get_sentence_vector(elt) for elt in web_res] + [
                self.em.get_sentence_vector(text=text)]
            vector = np.concatenate(all_vector)

            if vector.shape[0] == 2200:
                l_of_vectors.append(vector)
                l_of_labels.append(label)

        X = np.asmatrix(l_of_vectors)
        y = to_categorical(self.encoder.fit_transform(l_of_labels))

        if test_split:
            return train_test_split(X, y)
        else:
            return X, y

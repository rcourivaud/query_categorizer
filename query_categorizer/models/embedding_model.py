from query_categorizer.errors import NotAllResultsException
from query_categorizer.utils import clean_results
import fastText
import numpy as np


class EmbeddingModel(object):
    def __init__(self, path_to_model, label_prefix="__label__"):
        """

        :param path_to_model:
        :param label_prefix:
        """
        self.label_prefix = label_prefix
        self.path_to_model = path_to_model
        self.model = fastText.load_model(self.path_to_model)

    def get_feature_vector(self, query, results):
        """
        Create Feature vector using query and web results

        :param query:
        :param results:
        :return:
        """
        if len(results) == 10:
            all_res = [" ".join(elt.values()) for elt in clean_results(results)]
            all_vector = [self.get_sentence_vector(elt) for elt in all_res] + [
                self.get_sentence_vector(query)]
            vector = np.concatenate(all_vector)
            return vector
        else:
            raise NotAllResultsException("You must give 10 web results...")

    def predict(self, text):
        """
        Predict the label of text using pretrained model vector

        :param text:
        :return:
        """
        return self.predictk(text=text, k=1)

    def predictk(self, text, k):
        """
        Return K multi  labels prediction

        :param text:
        :param k:
        :return:
        """
        prediction = self.model.predict(text=text, k=k)
        return [elt.replace(self.label_prefix, "") for elt in prediction[0]], [float(elt) for elt in prediction[1]]

    def get_sentence_vector(self, text):
        """
        Get sentence representation of text

        :param text:
        :return:
        """
        return self.model.get_sentence_vector(text=text)

    def train(self, file_name, epoch=10, word_n_gram=2, dimension=200):
        """
        Train FastText supervised model

        :param file_name:
        :param epoch:
        :param word_n_gram:
        :param dimension:
        :return:
        """
        model = fastText.train_supervised(file_name,
                                          epoch=epoch,
                                          wordNgrams=word_n_gram,
                                          dim=dimension, )
        model.save_model(self.path_to_model)
        return model

    def load(self):
        """

        :return: fast text model loaded
        """
        return fastText.load_model(self.path_to_model)

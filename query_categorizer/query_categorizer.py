# -*- coding: utf-8 -*-
import os

from .utils import clean_results
from .get_results import get_qwant_result
from .models.bagging_model import BaggingModel
from .models.embedding_model import EmbeddingModel
import numpy as np
from sklearn.externals import joblib

"""Main module."""


class QueryCategorizer(object):
    def __init__(self):
        path_dir = os.path.dirname(os.path.realpath(__file__))

        embedding_model = os.path.join(path_dir, "res/model_categories.bin")
        self.em = EmbeddingModel(path_to_model=embedding_model)
        self.encoder = joblib.load(os.path.join(path_dir, "res/label_encoder.pkl"))

        self.bm = BaggingModel(path_to_embedding_model=embedding_model, encoder=self.encoder)
        self.model = self.bm.load_bagging_model(path_to_model=os.path.join(path_dir,
                                                                           "res/bagging_queries.h5"))
        self.labels = self.em.model.get_labels()

    def predict_query(self, query):
        web_results = clean_results(get_qwant_result(query))
        return self.predict_query_results(query=query, results=web_results)

    def predict_query_results(self, query, results, k=10):
        vector = self.em.get_feature_vector(query, results)
        predictions = self.model.predict(vector.reshape(1, vector.shape[0]))
        label = self.encoder.inverse_transform(np.argmax(predictions))
        proba = np.max(predictions)
        return label, proba, self.em.predictk(text=query, k=k)

    def get_labels(self):
        return list(self.encoder.classes_)

    def process_query(self, query, results=None):
        if results is None:
            results = clean_results(get_qwant_result(query))

        label, proba, embedding_prediction = self.predict_query_results(query, results)
        return {
            "label": str(label),
            "probability": float(proba),
            "embedding_prediction": {"labels": embedding_prediction[0], "probabilities": embedding_prediction[1]},
            "embedding_vector": [float(elt) for elt in self.em.get_sentence_vector(text=query)],
            "labels": self.labels
        }

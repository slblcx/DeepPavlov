"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import List

import scipy as sp
from scipy import sparse

from deeppavlov.core.models.component import Component
from deeppavlov.core.models.serializable import Serializable
from deeppavlov.core.common.log import get_logger
from deeppavlov.core.common.registry import register
from sklearn.feature_extraction.text import TfidfVectorizer
from deeppavlov.core.common.file import save_pickle
from deeppavlov.core.common.file import load_pickle
from deeppavlov.core.commands.utils import expand_path

TOKENIZER = None
logger = get_logger(__name__)


@register('tfidf_vectorizer')
class TfIdfVectorizer(Component, Serializable):

    def __init__(self, save_path: str = None, load_path: str = None, **kwargs):

        self.save_path = save_path
        self.load_path = load_path
        if kwargs['mode'] == 'train':
            self.tfidf_vect = TfidfVectorizer()
        else:
            self.load()



    def __call__(self, questions: List[str]) -> sp.sparse.csr_matrix:
        q_vects = self.tfidf_vect.transform(questions)

        return q_vects



    def fit(self, x_train) -> None:
        self.w_matrix = self.tfidf_vect.fit_transform(x_train)

    def save(self) -> None:
        logger.info("Saving tfidf vectorizer to {}".format(self.save_path))
        save_pickle((self.w_matrix, self.tfidf_vect), expand_path(self.save_path))


    def load(self) -> None:
        logger.info("Loading tfidf vectorizer from {}".format(self.load_path))
        self.w_matrix, self.tfidf_vect = load_pickle(expand_path(self.load_path))

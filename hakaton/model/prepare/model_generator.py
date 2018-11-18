from typing import Tuple

import pandas as pd
from sklearn.utils import shuffle
from tensorflow import keras

from hakaton.corpus.corpus import Corpus
from hakaton.img.img_reader import ImgReader

META_SRC = "./dataset/train/0_0_0_metadata_extended.csv"
ROOT_DIR = "./dataset/train"
IS_SHUFFLE = True
TRAIN_LABEL = "type"

train_meta_df = pd.read_csv(META_SRC)
if IS_SHUFFLE:
    train_meta_df = shuffle(train_meta_df)


def reshape_to_dense(imgs):
    return imgs.reshape((imgs.shape[0], -1))


img_reader = ImgReader()
corpus = Corpus(img_reader, META_SRC, ROOT_DIR)
imgs, types = corpus.get_all_images_with_column(TRAIN_LABEL, IS_SHUFFLE)
types = keras.utils.to_categorical(y=types)
imgs = reshape_to_dense(imgs)


class ModelGenerator:
    def __init__(self, model, corpus: Corpus, img_reader: ImgReader):
        self._model = model
        self._corpus = corpus
        self._img_reader = img_reader

    def generate(self, train_label: str, is_shuffle=True, flatten=True, epochs=1, batch_size=16, validation_split=None):
        imgs, labels = self._corpus.get_all_images_with_column(train_label, is_shuffle)
        if flatten:
            imgs = imgs.reshape((imgs.shape[0], -1))
        labels_encoded = keras.utils.to_categorical(y=types)
        self._fit_model(imgs, labels_encoded, epochs, batch_size, validation_split)

        return self._model.model()

    def _fit_model(self, imgs, labels_encoded, epochs=1, batch_size=16, validation_split=None):
        model: keras.Model = self._model.model()
        model.fit(imgs, labels_encoded, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

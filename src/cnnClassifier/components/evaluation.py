from src.cnnClassifier.entity.config_entity import EvaluationConfig
from pathlib import Path
import tensorflow as tf
from src.cnnClassifier.utils.utils import save_json


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.score = None
        self.model = None
        self.config = config

    def _valid_generator(self):
        data_generator_kwargs = dict(
            rescale=1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation='bi-linear'
        )

        valid_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            **data_generator_kwargs
        )

        self.valid_generator = valid_generator.flow_from_directory(
            directory=self.config.training_data,
            subset='validation',
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

    def evaluation(self):
        model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = model.evaluate(self.valid_generator)

    def save_score(self):
        scores = {'loss': self.score[0], 'accuracy': self.score[1]}
        save_json(path=Path('scores.json'), data=scores)

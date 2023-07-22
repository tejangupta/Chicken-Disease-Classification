from src.cnnClassifier.entity.config_entity import PrepareCallbacksConfig
import time
import os
import tensorflow as tf


class PrepareCallback:
    def __init__(self, config: PrepareCallbacksConfig):
        self.config = config

    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(
            self.config.tensorboard_root_log_dir,
            f"tb_logs_at_{timestamp}",
        )
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)

    @property
    def _create_ckpt_callbacks(self):
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=str(self.config.checkpoint_model_filepath),
            save_best_only=True
        )

    @property
    def _create_early_stopping(self):
        return tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )

    @property
    def _create_lr_scheduler(self):
        def scheduler(epoch, lr):
            if epoch % 10 == 0 and epoch > 0:
                lr = lr / 2
            return lr

        return tf.keras.callbacks.LearningRateScheduler(scheduler)

    def get_tb_ckpt_callbacks(self):
        return [
            self._create_tb_callbacks,
            self._create_ckpt_callbacks,
            self._create_early_stopping,
            self._create_lr_scheduler
        ]

import time
from gensim.models.callbacks import CallbackAny2Vec


class CustomCallback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 1
        self.loss_to_be_subed = 0
        self.start = time.time()

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subed
        self.loss_to_be_subed = loss
        if self.epoch % 10 == 0:
            print(f'Loss after epoch {self.epoch}: {loss_now} / Duration: {time.time()-self.start:.3f}')
        elif self.epoch % 10 == 1:
            self.start = time.time()
        self.epoch += 1

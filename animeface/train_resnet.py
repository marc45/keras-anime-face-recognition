from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import preprocess_input
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import datasets
import resnet

batch_size = 32
nb_classes = 10
nb_epoch = 200
img_rows, img_cols, img_channels = 32, 32, 3

def run():
    (X_train, y_train), (X_test, y_test) = datasets.load_data(img_rows, img_cols)
    X_train = preprocess_input(X_train)
    X_test = preprocess_input(X_test)
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    model = resnet.ResnetBuilder.build_resnet_18((img_channels, img_rows, img_cols), nb_classes)
    model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
    checkpointer = ModelCheckpoint(filepath="/tmp/resnet50.h5", monitor="val_acc", verbose=1, save_best_only=True)
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images
    datagen.fit(X_train)
    model.fit_generator(datagen.flow(X_train, Y_train,
                                     batch_size=batch_size),
                        samples_per_epoch=X_train.shape[0],
                        callbacks=[checkpointer],
                        nb_epoch=nb_epoch,
                        validation_data=(X_test, Y_test))

if __name__ == "__main__":
    run()

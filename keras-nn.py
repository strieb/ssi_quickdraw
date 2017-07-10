import sys
if not hasattr(sys, 'argv'):
    sys.argv  = ['']
import numpy as np
import json
from tensorflow.contrib.keras.python.keras.models import Sequential, load_model, model_from_json
from tensorflow.contrib.keras.python.keras.layers import Dense, Dropout, Activation
from tensorflow.contrib.keras.python.keras.optimizers import SGD, Adam, RMSprop
from tensorflow.contrib.keras.python.keras.utils import np_utils
from tensorflow.contrib.keras.python.keras.callbacks import TensorBoard

def getOptions(opts, vars):

    vars['model'] = None

    opts['model_path'] = ''
    opts['batch_size'] = 128
    opts['n_epoch'] = 10
    opts['validation_split'] = 0.5
    opts['verbose'] = 1
    opts['class_weight'] = ''


def train(x, y, scores, opts, vars):

    n_input = x[0].dim
    n_output = max(y)+1

    if opts['model_path'].endswith('.json'):

        print ('load model architecture from ' + opts['model_path'])		
        model = model_from_json (open (opts['model_path']).read())

    elif opts['model_path'].endswith('.py'):

        print ('load model architecture from ' + opts['model_path'])
        module = __import__(opts['model_path'][:-3])
        model = module.getModel(n_input, n_output)

    else:

        print ('using default model architecture')
        model = Sequential()
        model.add(Dense(n_output, input_shape=(n_input,)))        
        model.add(Dense(n_output))
        model.add(Activation('softmax'))

    model.summary()
    model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])
    
    train_x = np.empty((len(x), n_input))
    train_y = np.empty((len(y), n_output))

    train_x = train_x.reshape(train_x.shape[0],32,32,1)

    for sample in range(len(x)):
        label = convert_to_one_hot(y[sample], n_output)
        train_x[sample]  = np.reshape(x[sample],(32,32,1))
        train_y[sample] = label

    train_x = train_x.astype('float32')

    if not opts['class_weight']:
        class_weight = None
    else:
        tmp = opts['class_weight'].split(',')
        class_weight = {}
        for i in range(n_output):    
            class_weight[i] = tmp[i]
        print('using class weights: ' + str(class_weight))
    
    tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
                          write_graph=True, write_images=False)

    model.fit(train_x, 
              train_y, 
              epochs=opts['n_epoch'],
              validation_split=opts['validation_split'],
              class_weight=class_weight,
              verbose=opts['verbose'],
              callbacks=[tensorboard])

    vars['model'] = model


def forward(x, probs, opts, vars):
	
    n_input = x.dim

    model = vars['model']

    if model is None:

        path = vars['model_path']
        print ('load model from ' + path)		    
        model = model_from_json (open (path + '.json').read())
        model.load_weights(path)
        vars['model'] = model

    if not model is None:

        np_array_x = np.asarray(x)
        np_array_x = np_array_x.astype('float32')
        np_array_x = np.reshape(np_array_x, (1, 32,32,1))
        pred = model.predict(np_array_x)
        for i in range (len(pred[0])):
            probs[i] = float(pred[0][i])

    else:

        print('WARNING: train model first')


def save(path, opts, vars):

    if not vars['model'] is None:

        print('save model to ' + path)

        vars['model'].save_weights(path)
        json_string = vars['model'].to_json()
        json_pretty = json.loads(json_string)
        open (path + '.json', 'w').write(json.dumps(json_pretty, indent=4, sort_keys=True))

    else:

        print('WARNING: train model first')


def load(path, opts, vars):

    # we load the model at first forward call
    # https://github.com/fchollet/keras/issues/2397
    
    #print ('load model from ' + path)		    
    #model = model_from_json (open (path + '.json').read())
    #model.load_weights(path)

    #vars['model'] = model;
    
    vars['model_path'] = path
    vars['model'] = None


### HELPER ###

def convert_to_one_hot(label, n_classes):

    float_label = int(label)
    one_hot = np.zeros(n_classes)
    one_hot[label] = 1.0
    return one_hot


if __name__ == '__main__' :
    train(0,0)

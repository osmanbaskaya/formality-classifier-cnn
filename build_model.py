import sys
import data
import codecs
import cPickle
import os
from model import create_logistic_model, create_regression_model, train_model


fn = sys.argv[1]
model_output_dir = sys.argv[2]
problem_type = sys.argv[3]
use_pretrained_embeddings = True if sys.argv[4].lower() == 'true' else False

print >> sys.stderr, fn, model_output_dir, problem_type, use_pretrained_embeddings

assert problem_type in ('regression', 'classification'), "Problem type should be either regression or classification"

maxlen = 25  # maximum length for each sentence.
max_features = 25000  # length of the vocabulary.
batch_size = 32
nb_epoch = 4
additional_num_words = 2  # "UNK" and "PADDING"


(X_train, y_train), (_, _), word_idx = data.read(fn, 0.0, maxlen, max_features, problem_type)
print >> sys.stderr, 'X_train shape:', X_train.shape

max_features = min(max_features, len(word_idx) + additional_num_words)

if problem_type == 'regression':
    model = create_regression_model(maxlen, max_features, word_idx, use_pretrained_embeddings)
else:
    model = create_logistic_model(maxlen, max_features, word_idx, use_pretrained_embeddings)

train_model(model, X_train, y_train, batch_size, nb_epoch)
model.save_weights(os.path.join(model_output_dir, 'weights.h5'), overwrite=True)
print >> sys.stderr, "Weights are written"

cPickle.dump(word_idx, codecs.open(os.path.join(model_output_dir, 'word_idx.json'), 'w', encoding='utf8'))
print >> sys.stderr, "word_idx dict is written"

architecture = model.to_json()
open(os.path.join(model_output_dir, 'architecture.json'), 'w').write(architecture)
print >> sys.stderr, "Architecture is written"



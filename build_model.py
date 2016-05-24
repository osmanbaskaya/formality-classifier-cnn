import sys
import data
import codecs
import ujson
from model import create_logistic_model, create_regression_model, train_model


fn = sys.argv[1]
model_output_file = sys.argv[2]
problem_type = sys.argv[3]
use_pretrained_embeddings = True if sys.argv[4].lower() == 'true' else False


print >> sys.stderr, fn, model_output_file, problem_type, use_pretrained_embeddings


assert problem_type in ('regression', 'classification'), "Problem type should be either regression or classification"

maxlen = 20  # maximum length for each sentence.
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
model.save_weights(model_output_file)
word_idx_file = model_output_file + '-word_idx.json'
ujson.dump(word_idx, codecs.open(word_idx_file, 'w', encoding='utf8'))
architecture = model.to_json()
arch_file = model_output_file + '-arch.json'
open(arch_file, 'w').write(architecture)


print >> sys.stderr, "Model is saved in {}".format(model_output_file)
print >> sys.stderr, "Architecture is saved in {}".format(arch_file)
print >> sys.stderr, "word-idx matrix is saved in {}".format(arch_file)
# formality-classifier-cnn
CNN classifier for Formality in text.


### Cross Validation

In order to run cross validation on a dataset, you can just run:

```
make cross-validate-formality.lahiri.dataset NUM_FOLD=10 PROBLEM_TYPE=regression
```

`PROBLEM_TYPE` defines your problem, either regression or classification. Labels for `formality.lahiri.dataset` between -3 to 3 and real-valued. So, you should give `PROBLEM_TYPE=regression`.
`NUM_FOLD` determines how many fold you run for evaluation of the dataset. Important to note that dataset should be in datasets/ directory.

Example for a classification problem:

```
make cross-validate-formality.lahiri.classes.clean.dataset NUM_FOLD=10 PROBLEM_TYPE=classification
```

### Build and Save Model

Assume that we have formality datasets for emails and it is located in `datasets/formality-email`. You can run the following command; build and save a model in `pretrained-models` directory.

```
make pretrained-models/model-formality-email USE_PRETRAINED_EMBEDDINGS=False
```

If you want to use pretrained word embeddings (e.g., Word2Vec) then you can run this:

```
make pretrained-models/model-formality-email
```


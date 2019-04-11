# Deep Learning Notes
## softmax
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\softmax: x_i = \cfrac{e^{x_i}}{\sum_{i=1}^m e^{x_i}}">
</p>

## CNN
## RNN
## GRU
## LSTM
## Word2Vec
[Distributed Representations of Words and Phrases and their Compositionality, Tomas Mikolov, 2013](../papers/1310.4546.pdf)
### skip-grams
- context: one word
- target: a previous or next word skip n grams

### cbow
- context: previous or next n words
- target: one word

### negative sampling
1. select positive and negative smaples
2. only train the output neurals corresponding to training samples
3. turn into a binary classification problem

## Glove
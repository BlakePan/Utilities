# Machine Learning Notes
## Algorithms
### Linear Regression
#### model
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\h(x)=W'x+b">
</p>

#### loss
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\MSE = \cfrac{1}{2m} * \sum_{i=1}^m (h(x_i)-yi)^2">
</p>

#### gradient
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\cfrac{1}{m} * \sum_{i=1}^m(h(x_i)-y_i) * x_i">
</p>

### Logistic Regression
#### model
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\h(x) = g(W'x + b)">
</p>
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\sigmoid: g(x) = \cfrac{1}{1 + e^{-x}}">
</p>

#### loss
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\cfrac{1}{m} \sum(-y*log(h(x)) - (1-y)*log(1-h(x)))">
</p>

#### gradient
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\cfrac{1}{m} \sum(h(x)-y) * x">
</p>

<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\g'(x) = g(x)(1-g(x))">
</p>

### Decision Tree

### Random Forest

### Bagging

### Boosting

### K-Means

### K-NN

### SVM

## Training Methods
### Supervised Learning
A data set with know correct output (label)

- regression
	- predict results within a continuous output

- classification
	- predict results in a discrete output

### Unsupervised Learning
Unsupervised learning allows us to approach problems with little or no idea what our results should look like

- clustering
	- group by similarity of features

### gradient descent

<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\min\ L(W)">
</p>

<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\w_i = w_i - \alpha * \cfrac{\partial}{\partial w_i}  L(W)">
</p>


### Feature Scaling
Normalize feature

<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\x_i = \cfrac {x_i - \mu} {\sigma}">
</p>

<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\mu = avg(X)">
</p>

<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\sigma = std(X)">
</p>

### Lost Functions

- MSE
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\cfrac{1}{2m} * \sum (h(x)-y)^2">
</p>

- Logistic regression error
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\cfrac{1}{m} \sum(-y*log(h(x)) - (1-y)*log(1-h(x)))">
</p>

- cross entropy
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\cfrac{1}{m} \sum(-y*log(h(x)))">
</p>

### dynamic gradient clipping
### Batch normalization
### Dropout
### Regularization
- L1
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\lambda \sum_i |w_i|">
</p>

- L2
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\\lambda \sum_i w_i^2">
</p>
<p align="center">
  <img\lambda $$ selected by cross validation">
</p>

### cross validation
### Gradient Based Optimizers
### BPTT
### RL
- priority experience replay
- a3c

## Visualization
### t-sne

## Problems
### overfitting (high variance)
- Reduce the number of features
- Regularization
- Data augmentation
- Cross validation
- Early stopping
- Reduce Model Complexity
- Dropout


# Refs
[coursera: machine learning](https://www.coursera.org/learn/machine-learning)

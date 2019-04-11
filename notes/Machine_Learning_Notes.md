# Machine Learning Notes
## Algorithms
### Linear Regression
#### model
<p align="center">
  <img src="http://latex.codecogs.com/gif.latex?\\h(x)=W'x+b}">
</p>
#### loss
$$ MSE = \cfrac{1}{2m} * \sum (h(x)-y)^2 $$
#### gradient
$$ \cfrac{1}{m} * \sum(h(x_i)-y) * x $$

### Logistic Regression
#### model
$$ h(x) = g(W'x + b) $$

$$ sigmoid: g(x) = \cfrac{1}{1 + e^{-x}} $$
#### loss
$$ \cfrac{1}{m} \sum(-y*log(h(x)) - (1-y)*log(1-h(x))) $$
#### gradient
$$ \cfrac{1}{m} \sum(h(x)-y) * x $$

$$ g'(x) = g(x)(1-g(x))$$

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

$$ min\ L(W) $$

$$ w_i = w_i - \alpha * \cfrac{\partial}{\partial w_i}  L(W) $$ 


### Feature Scaling
Normalize feature

$$ x_i = \cfrac {x_i - \mu} {\sigma} $$

$$ \mu = avg(X) $$

$$ \sigma = std(X) $$

### Lost Functions

- MSE

$$ \cfrac{1}{2m} * \sum (h(x)-y)^2 $$

- Logistic regression error

$$ \cfrac{1}{m} \sum(-y*log(h(x)) - (1-y)*log(1-h(x))) $$

- cross entropy

$$ \cfrac{1}{m} \sum(-y*log(h(x))) $$

### dynamic gradient clipping
### Batch normalization
### Dropout
### Regularization
- L1

$$ \lambda \sum_i |w_i|$$

- L2

$$ \lambda \sum_i w_i^2 $$

$$ \lambda $$ selected by cross validation

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

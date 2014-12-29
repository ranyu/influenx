import graphlab as gl
dataset = gl.SFrame('http://s3.amazonaws.com/GraphLab-Datasets/mnist/sframe/train6k')
net = gl.deeplearning.create(dataset, 'label')
model = gl.neuralnet_classifier.create(dataset, 'label', network=net)
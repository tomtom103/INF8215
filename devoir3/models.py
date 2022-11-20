import nn
import backend
import numpy as np


class PerceptronModel(object):
    def __init__(self, dimensions: int):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self._dimensions = dimensions
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        return nn.DotProduct(self.w,x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        return 1 if nn.as_scalar(self.run(x)) >= 0 else -1

    def train(self, dataset: backend.PerceptronDataset):
        """
        Train the perceptron until convergence.
        """
        converged = False
        while not converged:
            converged = True   
            for x, y in dataset.iterate_once(1):
                y_hat = self.get_prediction(x)
                if y_hat != nn.as_scalar(y):
                    self.w.update(x, nn.as_scalar(y))
                    converged = False


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self):
        # Initialize your model parameters here
        self.batch_size = 200
        self.num_hidden_layers = 3

        self.w = nn.Parameter(1, self.num_hidden_layers) # weights 
        self.b = nn.Parameter(1, self.num_hidden_layers) # biases 

        self.w_m = nn.Parameter(self.num_hidden_layers, self.num_hidden_layers)
        self.b_m = nn.Parameter(1, self.num_hidden_layers)

        # Output layers
        self.w_o = nn.Parameter(self.num_hidden_layers, 1)
        self.b_o = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        trans = nn.Linear(x, self.w)
        predicted_y = nn.AddBias(trans, self.b)
        relu = nn.ReLU(predicted_y)

        trans_m= nn.Linear(relu, self.w_m)
        predicted_y = nn.AddBias(trans_m, self.b_m)
        relu = nn.ReLU(predicted_y)

        trans_o = nn.Linear(relu,self.w_o)
        return nn.AddBias(trans_o, self.b_o)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset: backend.RegressionDataset):
        """
        Trains the model.
        """
        base_rate = -0.1
        while True:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients(loss, [self.w, self.b, self.w_m, self.b_m,self.w_o, self.b_o])

                learning_rate = np.minimum(-0.004, base_rate)

                # print(learning_rate)
                self.w.update(gradients[0], learning_rate)
                self.b.update(gradients[1], learning_rate)
                self.w_m.update(gradients[2], learning_rate)
                self.b_m.update(gradients[3], learning_rate)
                self.w_o.update(gradients[4], learning_rate)
                self.b_o.update(gradients[5], learning_rate)
            
            base_rate += 0.01
            loss = self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))
            if nn.as_scalar(loss) < 0.02:
                return


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"

import Orange


class Classifier:

    def __init__(self):

        base_learners = [
            Orange.classification.knn.kNNLearner(k=5),
            Orange.classification.neural.NeuralNetworkLearner(max_iter=1000, n_mid=50),
            Orange.ensemble.forest.RandomForestLearner(trees=200, attributes=7),
            Orange.classification.tree.TreeLearner(max_depth=225)
        ]

        meta_learner=Orange.classification.neural.NeuralNetworkLearner()

        self.learner = Orange.ensemble.stacking.StackedClassificationLearner(base_learners, meta_learner=meta_learner)
        self.classifier = None

    def train(self, samples):
        self.classifier = self.learner(samples)
        self.learner = None

    def classify(self, sample):
        return self.classifier(sample)


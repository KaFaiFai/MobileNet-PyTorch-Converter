import sklearn.metrics


class ClassificationMetrics:
    def __init__(self, truths, preds):
        self.truths = truths
        self.preds = preds

    @property
    def accuracy(self):
        return sklearn.metrics.accuracy_score(self.truths, self.preds)

    @property
    def precision(self):
        return sklearn.metrics.precision_score(self.truths, self.preds, average="macro", zero_division=0)

    @property
    def recall(self):
        return sklearn.metrics.recall_score(self.truths, self.preds, average="macro", zero_division=0)

    @property
    def f1_score(self):
        return sklearn.metrics.f1_score(self.truths, self.preds, average="macro", zero_division=0)

    def print_report(self):
        print(f"Accuracy: {self.accuracy:2.2%} | Precision: {self.precision:.4f}")
        print(f"Recall:   {self.recall:.4f} | F1 score:  {self.f1_score:.4f}")


def test():
    truths = [0, 2, 1, 3, 5, 3, 4, 2, 1, 3, 2]
    preds = [0, 2, 4, 0, 2, 3, 3, 3, 3, 1, 2]
    metrics = ClassificationMetrics(truths, preds)
    metrics.print_report()


if __name__ == '__main__':
    test()
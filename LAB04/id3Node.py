class ID3Node:
    def __init__(
        self,
        featureIndex=None,
        threshold=None,
        left=None,
        right=None,
        infGain=None,
        value=None,
    ):
        self.featureIndex = featureIndex
        self.threshold = threshold
        self.left = left
        self.right = right
        self.infGain = infGain
        self.value = value

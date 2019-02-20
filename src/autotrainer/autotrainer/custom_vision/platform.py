
from enum import Enum

class Platform(Enum):
    DOCKER = 1
    CORE_ML = 2
    TENSORFLOW = 3
    ONNX = 4

    def to_id(self):
        if self.value == Platform.Docker:
            return "DockerFile"
        if self.value == Platform.CORE_ML:
            return "CoreML"
        if self.value == Platform.TENSORFLOW :
            return "TensorFlow"
        if(self.value == Platform.ONNX):
            return "ONNX"
        else:
            return None

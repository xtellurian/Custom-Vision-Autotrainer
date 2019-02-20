
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

class Flavour(Enum):
    Linux = 1
    Windows = 2
    ONNX10 = 3
    ONNX12 = 4

    def to_id(self):
        if self.value == Flavour.Linux:
            return "Linux"
        if self.value == Flavour.Windows:
            return "Windows"
        if self.value == Flavour.ONNX10 :
            return "ONNX10"
        if(self.value == Flavour.ONNX12):
            return "ONNX12"
        else:
            return None

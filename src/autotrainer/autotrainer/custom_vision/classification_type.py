from enum import Enum
# 'Multiclass or Multilabel'
class ClassificationType(Enum):
    MULTICLASS = 1
    MULTILABEL = 2

    def to_id(self):
        if self.value == ClassificationType.MULTICLASS:
            return "Multiclass"
        if self.value == ClassificationType.MULTILABEL:
            return "Multilabel"
        else:
            return None

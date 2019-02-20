from enum import Enum

class Domain(Enum):
    GENERAL_CLASSIFICATION = 1
    GENERAL_CLASSIFICATION_COMPACT = 2
    GENERAL_OBJECT_DETECTION = 3
    FOOD_CLASSIFICATION = 4

    def to_id(self):
        if self.value == Domain.GENERAL_CLASSIFICATION:
            return "ee85a74c-405e-4adc-bb47-ffa8ca0c9f31"
        if self.value == Domain.GENERAL_CLASSIFICATION_COMPACT:
            return "0732100f-1a38-4e49-a514-c9b44c697ab5"
        if self.value == Domain.FOOD_CLASSIFICATION :
            return "c151d5b5-dd07-472a-acc8-15d29dea8518"
        if(self.value == Domain.GENERAL_OBJECT_DETECTION):
            return "a27d5ca5-bb19-49d8-a70a-fec086c47f5b"
        else:
            return None

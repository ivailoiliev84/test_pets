from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def validator_only_letters(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('The field must contain only letters!')


def validator_file_max_size_in_mb(max_size):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(max_size))

    return validate_image


@deconstructible
class ValidatorMaxSizeInMB:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        file_size = value.file.size
        if file_size > self.__convert_megabytes_to_bytes(self.max_size):
            raise ValidationError(self.__exception_message())

    def __convert_megabytes_to_bytes(self, value):
        return value * 1024 * 1024

    def __exception_message(self):
        return f"Max file size is {self.max_size:.f2}MB"

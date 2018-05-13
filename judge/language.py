class LANGUAGE(object):
    PYTHON = 'python'
    IMAGE_NAME_MAP = {}
    SOURCE_NAME_MAP = {}

    @classmethod
    def get_image_name(cls, language):
        return cls.IMAGE_NAME_MAP[language]

    @classmethod
    def get_source_name(cls, language):
        return cls.SOURCE_NAME_MAP[language]


LANGUAGE.IMAGE_NAME_MAP = {
    LANGUAGE.PYTHON: 'judge-python'
}

LANGUAGE.SOURCE_NAME_MAP = {
    LANGUAGE.PYTHON: 'code.py'
}

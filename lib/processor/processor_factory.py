import re


def _to_snake_case(name: str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _to_camel_case(name: str):
    return "".join(word.title() for word in name.split("_"))


class ProcessorFactory:
    def __init__(self, processor_name):
        self.processor_name = processor_name

    def get_processor(self):
        processors_module = __import__(
            "lib.processor.processors", fromlist=[_to_snake_case(self.processor_name)]
        )
        module = getattr(processors_module, _to_snake_case(self.processor_name))
        cls = getattr(module, _to_camel_case(self.processor_name))
        return cls

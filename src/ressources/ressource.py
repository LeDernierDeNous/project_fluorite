class Resource:
    def __init__(self, resource_type, resource_variant):
        self.resource_type = resource_type
        self.resource_variant = resource_variant

    def __repr__(self):
        return f"Resource({self.resource_type}, {self.resource_variant})"
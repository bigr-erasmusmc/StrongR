from sqlalchemy import types, String
import uuid

class UUID(types.TypeDecorator):
    impl = String()
    def __init__(self, *args, **kwargs):
        super(UUID, self).__init__(*args, **kwargs)
        self.impl.length = 64
        types.TypeDecorator.__init__(self,length=self.impl.length)

    def process_bind_param(self,value,dialect=None):
        if value and isinstance(value,uuid.UUID):
            return value
        elif value and not isinstance(value,uuid.UUID):
            raise ValueError,'value %s is not a valid uuid.UUID' % value
        else:
            return None

    def process_result_value(self,value,dialect=None):
        if value:
            return uuid.UUID(value)
        else:
            return None

    def is_mutable(self):
        return False

from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class ThemeAndLanguage(TypeDecorator):
    impl = VARCHAR(length=255)

    def process_bind_param(self, value, dialect):
        if not value:
            return '{}'
        elif not isinstance(value, dict):
            raise ValueError("ThemeAndLanguage expects a dictionary")
        else:
            try:
                value_dict = {key: val for key, val in value.items() if key == 'theme' or key == 'language'}
                return json.dumps(value_dict)
            except Exception as exc:
                print(f'error converting python objects to json data: {exc}')
    
    def process_result_value(self, value, dialect):
        try:
            if not value:
                return {}
            return json.loads(value)
        except Exception as exc:
            print(f'error converting json data to python objects: {exc}')

IS_UNIVERSAL_PARAM_VALUES = ["true", "false"]

def validate_is_universal_param(param: str):
    if param.lower() not in IS_UNIVERSAL_PARAM_VALUES:
        raise ValueError(f"Value {param} not accept to isUniversal parameter.")

    
def requiredFieldMissing(field_name: str) -> str:
    return f"{field_name} is required."

def unknownValue(field_name: str, value) -> str:
    return f"Unrecognized {field_name}: {str(value)}"
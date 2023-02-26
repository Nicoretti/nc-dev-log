def command(*args) -> str:
    """Transform all args into a single command string"""
    args = (str(arg) for arg in args)
    return f"{' '.join(args)}"

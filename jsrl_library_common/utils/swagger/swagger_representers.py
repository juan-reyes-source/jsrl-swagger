def str_quote_representer(dumper, data):
    """Generate string with double quoute in the swagger yaml

    Args:
        - dumper (Dumper): the yaml Dumper class
        - data (str): the string to export in the yaml file with double quote

    Returns:
        - ScalarNode: the scalar node to use when the object type related was founded
    """
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

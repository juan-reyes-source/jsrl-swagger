import yaml
from jsrl_library_common.utils.data.yaml import extend_yaml_from_file, export_yaml
from jsrl_library_common.constants.swagger import swagger_constants as swagger_cnts
from jsrl_library_common.utils.swagger.swagger_representers import str_quote_representer

def generate_yaml_file(specifications,
                       filename,
                       sort_keys=False):
    """Generate the yaml file to swagger definition

    Args:
        - specifications (dict): the swagger specifications
        - filename (str): the swagger file name
        - sort_keys (bool): do keys must be sorted?

    Returns:
        - str: the swagger file content in yaml format
    """
    dumper = yaml.dumper.SafeDumper
    dumper.ignore_aliases = lambda *args: True
    dumper.add_representer(swagger_cnts.QuotedStr, str_quote_representer)
    result = export_yaml(specifications,
                         filename,
                         dumper=dumper)

    return result


def extend_yaml(source_yaml,
                new_info_path):
    """Extend a yaml definition with yaml file

    Args:
        - source_yaml (dict): the yaml to extend
        - new_info_path (str): the path where the new yaml specifications was stored

    Raises:
        - FileNotFoundException
        
    Returns:
        - dict: the extended yaml
    """
    return extend_yaml_from_file(source_yaml, new_info_path)
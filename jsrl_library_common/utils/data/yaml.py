import yaml
from jsrl_library_common.utils.data.files import save_file_content
from jsrl_library_common.exceptions.files import files_exceptions as files_except

def load_yaml(filepath):
    """Load yaml from file

    Args:
        - filepath (str): the yaml file path

    Raises:
        - FileNotFoundException

    Returns:
        - Any: the yaml content
    """
    yaml_spec = {}
    with open(filepath, "r") as f:
        yaml_spec = yaml.safe_load(f)

    if not yaml_spec:
        raise files_except.FileNotFoundException(filepath,
                                                 "The info to add doesn't exist in path defined")
    
    return yaml_spec


def extend_yaml_from_file(source_yaml,
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
    extensions_spec = load_yaml(new_info_path)
    return _extend_yaml(source_yaml,
                        extensions_spec)


def extend_yaml(source_yaml,
                *extensions_spec):
    """Extend a yaml definition with multiple yaml specifications

    Args:
        - source_yaml (dict): the yaml to extend
        - *extensions_spec (tuple): the specification to add

    Raises:
        - FileNotFoundException
        
    Returns:
        - dict: the extended yaml
    """
    yaml_spec = source_yaml
    for spec in extensions_spec:
        yaml_spec = _extend_yaml(yaml_spec, spec)
    return yaml_spec


def export_yaml(specifications,
                filename,
                **dump_attributes):
    """Export a yaml specification in specific file

    Args:
        - specifications (dict): the yaml specification to store
        - filename (str): the file where the specification will be stored
        - **dump_attributes (dict): the export yaml additional configurations
            - indent (int): default 2
            - sort_keys (bool): default False
            - dumper (yaml.Dumper): default SafeDumper

    Returns:
        - dict: the exported specifications
    """
    dumper = dump_attributes.pop("dumper")
    if not dumper:
        dumper = yaml.dumper.SafeDumper
        dumper.ignore_aliases = lambda *args: True
    
    indent = dump_attributes.pop("indent", 2)
    sort_keys = dump_attributes.pop("sort_keys", False)
    result = yaml.dump(specifications,
                       indent=indent,
                       Dumper=dumper,
                       sort_keys=sort_keys,
                       **dump_attributes)
    
    save_file_content(filename,
                      result)
    return result



def _extend_yaml(source_specs,
                 new_info_specs):
    """Add the new specification to source yaml

    Args:
        - source_specs (dict): the source yaml specification
        - new_info_specs (dict): the yaml specification to add

    Returns:
        - Any: the extended specification
    """
    if type(source_specs) is not dict:
        return source_specs
    
    for spec_key in new_info_specs:
        if not source_specs.get(spec_key):
            source_specs[spec_key] = new_info_specs[spec_key]
        else:
            source_specs[spec_key] = _extend_yaml(source_specs[spec_key],
                                                  new_info_specs[spec_key])
    
    return source_specs
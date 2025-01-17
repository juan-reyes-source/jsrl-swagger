from os import PathLike
from flask import Blueprint
from typing import Any

class SwaggerFlaskBlueprint(Blueprint):
    """Extend the origin Blueprint class to support the swagger \
    logic

    Additional arguments:
        - swagger_tag_name (str|None): the name of the swagger tag related to this blueprint
        - swagger_tag_description (str|None): the description of swagger tag
        - swagger_schemas_modules (list): the swagger schemas modules
    """

    def __init__(self, 
                 name: str, 
                 import_name: str, 
                 static_folder: str | PathLike[str] | None = None,
                 static_url_path: str | None = None,
                 template_folder: str | PathLike[str] | None = None,
                 url_prefix: str | None = None,
                 subdomain: str | None = None,
                 url_defaults: dict[str, Any] | None = None,
                 root_path: str | None = None,
                 cli_group: str | None = ...,
                 swagger_tag_name: str | None = None,
                 swagger_tag_description: str | None = None,
                 swagger_schemas = None) -> None:
        """Extend the normal Blueprint with swagger definition
        """
        self.swagger_tag_spec = self._register_swagger_tag(name,
                                                           swagger_tag_name,
                                                           swagger_tag_description)
        self.swagger_schemas_modules = swagger_schemas
        super().__init__(name,
                         import_name,
                         static_folder,
                         static_url_path,
                         template_folder,
                         url_prefix,
                         subdomain,
                         url_defaults,
                         root_path,
                         cli_group)
        
    
    def _register_swagger_tag(self,
                              blueprint_name,
                              swagger_tag_name=None,
                              swagger_tag_description=None):
        """Register blueprint like swagger tag

        Args:
            - blueprint_name (str): the name of flask blueprint
            - swagger_tag_name (str|None): the name of the swagger tag
            - swagger_tag_description (str|None): the description of the tag
        
        Returns:
            - str: the swagger tag name related to this blueprint
        """
        swagger_tag_spec = {"name": blueprint_name}
        if swagger_tag_name:
            swagger_tag_spec["name"] = swagger_tag_name

        if swagger_tag_description:
            swagger_tag_spec["description"] = swagger_tag_description

        return swagger_tag_spec

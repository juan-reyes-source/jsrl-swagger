from os import PathLike
from flask import Blueprint
from typing import Any
from jsrl_library_common.models.swagger.flask_swagger_models import FlaskSwagger

class SwaggerFlaskBlueprint(Blueprint):
    """Extend the origin Blueprint class to support the swagger \
    logic

    Additional arguments:
        - swagger_tag_name (str|None): the name of the swagger tag related to this blueprint
        - swagger_tag_description (str|None): the description of swagger tag
        - swagger_schemas (module): the swagger schemas module
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
        self.swagger = FlaskSwagger()
        self.swagger_tag_name = self._register_swagger_tag(name,
                                                           swagger_tag_name,
                                                           swagger_tag_description)
        self._register_swagger_schemas(swagger_schemas)
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

        self.swagger.register_swagger_tag(blueprint_name,
                                          **swagger_tag_spec)
        return swagger_tag_spec["name"]


    def _register_swagger_schemas(self, schemas):
        """Register the swagger schemas record by this blueprint

        Args:
            - schemas (module): the schemas python module
        """
        if schemas:
            schemas_cnts = [ schema for schema in dir(schemas) if not schema.startswith("_") ]
            for schema_cnts in schemas_cnts:
                schema = getattr(schemas,
                                 schema_cnts)
                self.swagger.register_swagger_schema(schema)

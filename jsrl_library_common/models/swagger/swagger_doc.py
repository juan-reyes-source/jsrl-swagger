from jsrl_library_common.schemas import swagger as swagger_schemas
from jsrl_library_common.constants.swagger import swagger_constants as swagger_cnts
from jsrl_library_common.constants.swagger import swagger_security_schemas
from jsrl_library_common.utils.swagger.swagger_file import generate_yaml_file

class BuildSwaggerDoc:
    """Build the swagger documentation to api
    """

    _specifications = {}

    def __init__(self,
                 api_title="",
                 api_version="0.0.1") -> None:
        """Initialize the swagger docs component

        Args:
            - api_tile (str): the document swagger title
            - api_version (str): the version of API
        """
        self._specifications = {
            "openapi": "3.0.0",
            "info": {
                "title": api_title,
                "description": swagger_cnts.SwaggerMessages.REPLACE_VALUE.value,
                "version": api_version
            },
            "servers": [
                {
                    "url": swagger_cnts.BASE_LINK,
                    "description": "Default server"
                }
            ]
        }

        self._default_schemas_module = swagger_schemas
        self._default_security_schemas_module = swagger_security_schemas
        self.__register_default_schemas()
        self._register_default_security_schemas()


    def build(self, filename):
        """Generate the swagger file and store in the filename

        Args:
            - filename (str): the filename path where swagger will be generated

        Returns:
            - str: the swagger definition
        """
        return generate_yaml_file(self._specifications, filename)


    def set_api_general_info(self,
                             api_title,
                             api_version,
                             api_description=None):
        """Set the swagger API information

        Args:
            - api_title (str): the swagger document title
            - api_version (str): the api version
            - api_description (str|None): the api description
        """
        self._specifications["info"]["title"] = api_title
        self._specifications["info"]["version"] = api_version
        if api_description:
            self._specifications["info"]["description"] = api_description


    def set_servers(self,
                    servers,
                    override=True):
        """Set the API servers supported

        Args: 
            - servers (list[dict]): the servers to register
            - override (bool): are the current servers deleted?
        """
        new_servers = []
        for server in servers:
            new_servers.append({
                "url": server["url"],
                "description": server["description"]
            })
        
        if not override:
            new_servers += self._specifications["servers"]
        
        self._specifications["servers"] = new_servers
            

    def register_swagger_path(self,
                              path,
                              method,
                              paths_attributes):
        """Add or update a path defined in the swagger specification

        Args:
            - path (str): the url path of endpoint
            - method (str): the path method
            - paths_attributes (dict): the path specification attributes
        """
        path_spec = self._build_swagger_path_specification(path,
                                                           method,
                                                           paths_attributes)
        self._specifications["paths"][path] = path_spec


    def register_swagger_paths(self,
                               paths):
        """Add or update paths specification information

        Args:
            - paths (dict): the new paths specification information
                - key: the url path
                - value: dictionary with the following structure
                    - key: the endpoint method
                    - value: the path method specifications
        """
        for path in paths:
            for method in paths[path]:
                path_spec = self.__build_swagger_path_specification(path,
                                                                    method,
                                                                    paths[path][method])
                self._specifications["paths"][path] = path_spec


    def register_swagger_tags(self,
                              tags):
        """Register in the specifications the swagger tags

        Args:
            - tags (list[dict]): the tags to register
        """
        self._specifications["tags"] = [
            self.__build_swagger_tag_specification(tags[tag])
            for tag in tags
        ]


    def register_swagger_component_schema(self,
                                          schema):
        """
        """
        components = self._specifications.get("components", {"schemas": {}})
        schema_spec, schema_name = self.__build_swagger_components_schema(schema)
        components["schemas"][schema_name] = schema_spec
        self._specifications["components"] = components
        schema_ref_name = self._get_swagger_schema_ref(schema["$id"])
        print(f"Schema {schema_name}: registered successfully. ({schema_ref_name})")
        return schema_ref_name
    

    def register_swagger_paths_request_bodies(self, path_request_bodies):
        """
        Args:
            - path_request_bodies (dict): 
                - url
                    - method
                        - mime-type
                        - refs
        """
        for url in path_request_bodies:
            for method in path_request_bodies[url]:
                request_bodies = self._specifications["paths"][url][method].get("requestBody", {"content": {}})
                request_body_method = path_request_bodies[url][method]
                request_body = self.define_request_body_with_ref(request_body_method["mime-type"],
                                                                 request_body_method["refs"])
                request_bodies["content"] = {
                    **request_bodies["content"],
                    **request_body
                }
                self._specifications["paths"][url][method]["requestBody"] = request_bodies


    def register_swagger_security_schemas(self, value):
        """
        """



    def transform_tag_name(self, tag):
        """
        """
        return tag.replace("_", " ")\
                  .title()
    
    
    def transform_snake_to_lower_camel_case(self, value: str):
        """
        """
        words = value.strip().split("_")
        if len(words) > 1:
            words = [words[0]] + [word.title() for word in words[1:]]
        return ''.join(words)


    def define_path_params(self,
                           name,
                           data_type,
                           description,
                           required=True,
                           additional_schema_rules={}):
        """Define the swagger specification to parameters pass by path

        Args:
            - name (str): the name of parameter
            - data_type (str): the type of data pass by parameter
            - description (str): the parameter description
            - required (bool): is parameter required?
            - additional_schema_rules (dict): the schema validations

        Returns:
            - dict: the swagger specification
        """
        specification_additionals = {}

        for key in ["examples", "allowEmptyValue"]:
            if additional_schema_rules.get(key):
                specification_additionals[key] = additional_schema_rules.pop(key)

        return {
            "in": "path",
            "name": name,
            "description": description,
            "required": required,
            "schema": {
                "type": data_type,
                **additional_schema_rules
            },
            **specification_additionals
        }

    
    def define_query_params(self,
                            name,
                            data_type,
                            description,
                            allow_reserved=True,
                            required=True,
                            additional_schema_rules={}):
        """Define the swagger specification to parameters pass by query params

        Args:
            - name (str): the name of parameter
            - data_type (str): the type of data pass by parameter
            - description (str): the parameter description
            - allow_reserved (bool): is query parameter a non-percent-encoded?
            - required (bool): is parameter required?
            - additional_schema_rules (dict): the schema validations

        Returns:
            - dict: the swagger specification
        """
        specification_additionals = {}

        for key in ["examples", "allowEmptyValue"]:
            if additional_schema_rules.get(key):
                specification_additionals[key] = additional_schema_rules.pop(key)

        return {
            "in": "query",
            "name": name,
            "description": description,
            "required": required,
            "schema": {
                "type": data_type,
                **additional_schema_rules
            },
            "allowReserved": allow_reserved,
            **specification_additionals
        }


    def define_custom_headers(self,
                              name,
                              data_type,
                              description,
                              required=True,
                              additional_schema_rules={}):
        """Define the swagger specification to custom headers

        Args:
            - name (str): the name of parameter
            - data_type (str): the type of data pass by parameter
            - description (str): the parameter description
            - required (bool): is parameter required?
            - additional_schema_rules (dict): the schema validations

        Returns:
            - dict: the swagger specification
        """
        specification_additionals = {}

        for key in ["examples", "allowEmptyValue"]:
            if additional_schema_rules.get(key):
                specification_additionals[key] = additional_schema_rules.pop(key)

        return {
            "in": "header",
            "name": name,
            "description": description,
            "required": required,
            "schema": {
                "type": data_type,
                **additional_schema_rules
            },
            **specification_additionals
        }
    

    def define_request_body_with_ref(self,
                                     mimetype,
                                     components_ref):
        """
        """
        schema_refs = {"$ref": components_ref[-1]}
        if len(components_ref) > 1:
            schema_refs = {"oneOf": [{"$ref": ref} 
                           for ref in components_ref]}
        return {
            mimetype: {
                "schema": schema_refs
            }
        }
    

    def define_request_response_with_ref(self,
                                         status_code,
                                         mimetype,
                                         components_ref,
                                         description=None,
                                         examples=None):
        """
        """
        schema_refs = {"$ref": components_ref[-1]}
        if len(components_ref) > 1:
            schema_refs = {"oneOf": [{"$ref": ref}
                           for ref in components_ref]}
            
        status_code_spec = swagger_cnts.QuotedStr(status_code)
        response = {
            status_code_spec: {
                "content": {
                    mimetype: {
                        "schema": schema_refs
                    }
                }
            }
        }
        if description:
            response[status_code_spec]["description"] = description

        if examples:
            response[status_code_spec]["content"][mimetype]["examples"] = examples

        return response


    def define_path_security(self,
                             security):
        """Define the path security

        Args:
            - security (str|dict): the security configuration (custom scopes defined)

        Returns:
            - dict: the security specification
        """
        if type(security) is str:
            return {security: []}
        return security


    def define_security_api_key_schema(self,
                                       schema_name,
                                       name,
                                       additional_attributes={}):
        """Define the swagger specification to api key security schema

        Args:
            - schema_name (str): the schema alias to can refer in paths
            - name (str): the attribute name in headers
            - additional_attributes (dict): the additional schema specifications
        
        Returns:
            - dict: the schema swagger specification
        """
        return {
            schema_name: {
                "type": "apiKey",
                "in": "header",
                "name": name,
                **additional_attributes 
            }
        }
    

    def define_request_responses_options_method(self):
        """
        """
        return {
            "200": {
                "description": "200 response",
                "headers": {
                    "Access-Control-Allow-Origin": {
                        "schema": {
                            "type": "string"
                        }
                    },
                    "Access-Control-Allow-Methods": {
                        "schema": {
                            "type": "string"
                        }
                    },
                    "Access-Control-Allow-Headers": {
                        "schema": {
                            "type": "string"
                        }
                    }
                },
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object"
                        }
                    }
                }
            }
        }


    def _get_swagger_schema_name(self,
                                json_schema_id: str):
        """Extract the swagger schema name from json schema id

        Args:
            - json_schema_id (str): the json schema id

        Returns:
            - str: the swagger schema name
        """
        return json_schema_id.split("/")[-1]
    
    
    def _get_swagger_schema_ref(self,
                                json_schema_id: str):
        """Extract the swagger reference from json schema id

        Args:
            - json_schema_id (str): the json schema id

        Returns:
            - str: the swagger schema ref
        """
        return "#/components/" + '/'.join(json_schema_id.split("/")[-2:])


    def __build_swagger_tag_specification(self,
                                          tag):
        """Build the swagger specification structure to define a
        tag

        Args:
            - tag (dict): the tag information
        
        Returns:
            - dict: the swagger tag specification
        """
        return {
            "name": tag["name"],
            "description": tag.get("description", 
                                   swagger_cnts.SwaggerMessages.REPLACE_VALUE.value)
        }


    def _build_swagger_path_specification(self,
                                           path,
                                           method,
                                           path_attributes):
        """Build the swagger specification to path

        Args:
            - path (str): the endpoint path
            - method (str): the endpoint method
            - path_attributes (dict): the specification for this endpoint
                - summary (str): the endpoint summary
                - description (str|None): the endpoint complete description
                - tags (list[str]): the endpoint tags
                - operation_id (str): the endpoint swagger operation id
                - parameters (dict): the endpoint parameters
                - requestBody (dict): the endpoint request bodies
                - responses (dict): the endpoint responses

        Returns:
            - dict: the endpoint path specifications to specific method
        
        """
        DEFAULT_VALUE = swagger_cnts.SwaggerMessages.REPLACE_VALUE.value
        if not self._specifications.get("paths"):
            self._specifications["paths"] = {}

        path_spec = self._specifications["paths"].get(path, {})
        path_spec[method] = path_spec.get(method, {})
        path_spec[method] = {
            **path_spec[method],
            "summary": path_attributes["summary"],
            "description": path_attributes.get("description", DEFAULT_VALUE),
            "tags": path_attributes["tags"],
            "operationId": path_attributes["operation_id"]
        }

        for param in ["parameters", "security"]:
            if path_attributes.get(param):
                path_spec[method][param] = path_attributes[param]

        if path_attributes.get("requestBody"):
            path_spec[method]["requestBody"] = {
                "content": path_attributes["requestBody"]
            }

        if path_attributes.get("responses"):
            path_spec[method]["responses"] = path_attributes["responses"]

        return path_spec
    

    def __build_swagger_components_schema(self, schema):
        """Build the schema specification to can register in swagger
        components

        Args:
            - schema (dict): the schema in jsonschema format

        Returns:
            - dict: the schema specification
            - str: the schema name
        """
        schema_spec = {**schema}
        schema_spec.pop("$schema", None)
        schema_spec.pop("additionalProperties", None)
        schema_name = self._get_swagger_schema_name(schema_spec.pop("$id"))
        schema_spec = self.__adjust_swagger_schema_refs(schema_spec)
        return schema_spec, schema_name
        
    
    def __adjust_swagger_schema_refs(self, schema):
        """
        """
        if type(schema) is not dict:
            return schema
        if schema.get("$ref"):
            schema["$ref"] = self._get_swagger_schema_ref(schema["$ref"])
        
        if schema.get("allOf"):
            schema["allOf"] = [self.__adjust_swagger_schema_refs(ref) for ref in schema["allOf"]]
        
        elif schema.get("oneOf"):
            schema["oneOf"] = [self.__adjust_swagger_schema_refs(ref) for ref in schema["oneOf"]]
        
        elif schema.get("anyOf"):
            schema["anyOf"] = [self.__adjust_swagger_schema_refs(ref) for ref in schema["anyOf"]]
        
        if schema.get("properties"):
            schema["properties"] = {proper:self.__adjust_swagger_schema_refs(schema["properties"][proper])
                                    for proper in schema["properties"]}
        
        if schema.get("items"):
            schema["items"] = self.__adjust_swagger_schema_refs(schema["items"])

        return schema

    def __register_default_schemas(self):
        """
        """
        schema_module = self._default_schemas_module
        components = self._specifications.get("components",
                                              {"schemas": {}})
        schemas_cnts = [ schema for schema in dir(schema_module) if not schema.startswith("_") ]
        for schema_cnts in schemas_cnts:
            schema = getattr(schema_module,
                             schema_cnts)
            schema_spec, schema_name = self.__build_swagger_components_schema(schema)
            components["schemas"][schema_name] = schema_spec
            schema_ref_name = self._get_swagger_schema_ref(schema["$id"])
            print(f"Schema {schema_name}: registered successfully. ({schema_ref_name})")

        self._specifications["components"] = components


    def _register_default_security_schemas(self):
        """
        """
        schemas_module = self._default_security_schemas_module
        components = self._specifications.get("components", {})
        components["securitySchemes"] = components.get("securitySchemes", {})
        schemas_cnts = [ schema for schema in dir(schemas_module) if not schema.startswith("_") ]
        for schema_cnts in schemas_cnts:
            schema = getattr(schemas_module,
                             schema_cnts)
            components["securitySchemes"] = {
                **components["securitySchemes"],
                **schema
            }

        self._specifications["components"] = components


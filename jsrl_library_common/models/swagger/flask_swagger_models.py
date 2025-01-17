import yaml
from io import StringIO
from flask import Flask
from jsrl_library_common.models.swagger.singleton import SingletonMeta
from jsrl_library_common.models.swagger.swagger_doc import BuildSwaggerDoc
from jsrl_library_common.models.swagger.flask_swagger_blueprint import SwaggerFlaskBlueprint


class FlaskSwagger(metaclass=SingletonMeta):

    def __init__(self, app=None) -> None:
        """Initialize the FlaskSwagger class

        Args:
            - app (Flask): the flask application
        """
        self._app: Flask = app
        self._tags = {}
        self._endpoints = {}
        self.swagger_builder = BuildSwaggerDoc()
        self.endpoint_docs_groups = {
            "Path arguments": (self._extract_endpoint_path_params, "parameters"),
            "Long description": (self._extract_endpoint_description, "description"),
            "Query params": (self._extract_endpoint_query_params, "parameters"),
            "Custom headers": (self._extract_endpoint_custom_headers, "parameters"),
            "Request bodies": (self._extract_endpoint_request_bodies, "requestBody"),
            "Request responses": (self._extract_endpoint_request_responses, "responses"),
            "Security": (self._extract_endpoint_security, "security")
        }
        self._models = {}
        self._request_bodies = {}
        self._request_response = {}


    def set_app(self, app):
        """Set up the flask application

        Args:
            - app (Flask): the flask application
        """
        self._app = app

    
    def generate(self,
                 filename,
                 additional_methods=[]):
        """Generate the swagger specification and the swagger file

        Args:
            - filename (str): the swagger file
            - additional_methods (list): add the APIRestFull methods (OPTIONS, HEAD,...)

        Returns:
            - str: the swagger definition
        """
        print("...Extracting tags from blueprints...")
        self._extract_blueprints_information()
        print("...Extracting endpoints information...")
        self._extract_endpoints(additional_methods)
        self.swagger_builder.register_swagger_paths(self._endpoints)
        print("...Build yaml file...")
        return self.swagger_builder.build(filename)


    def register_swagger_builder(self, builder: BuildSwaggerDoc):
        """Set up the swagger builder

        Args:
            - builder (BuildSwaggerDoc): the swagger documentation builder
        """
        self.swagger_builder = builder


    def register_swagger_schema(self,
                                schema_info):
        """Register the schema in swagger components

        Args:
            - schema_info (dict): the schema info

        Returns:
            - str: the schema reference path
        """
        schema_ref_name = self.swagger_builder.register_swagger_component_schema(schema_info)
        self._models[schema_ref_name] = self._models.get(schema_ref_name, {})
        return schema_ref_name, schema_info["$id"].split("/")[-2:]


    def register_swagger_request_body(self,
                                      schema,
                                      schema_ref_name=None):
        """Register the request body schema in swagger components

        Args:
            - schema_info (dict): the schema info
            - schema_ref_name (str|None): the swagger schema ref

        Returns:
            - str: the schema reference path
        """
        if not schema_ref_name:
            schema_ref_name, schema_request_ref_name = self.register_swagger_schema(schema)
        self._request_bodies[schema_request_ref_name] = schema_ref_name
        return schema_ref_name
    

    def register_swagger_request_response(self,
                                          schema,
                                          schema_ref_name=None):
        """Register the request response schema in swagger components

        Args:
            - schema_info (dict): the schema info
            - schema_ref_name (str|None): the swagger schema ref

        Returns:
            - str: the schema reference path
        """
        if not schema_ref_name:
            schema_ref_name, schema_response_ref_name = self.register_swagger_schema(schema)
        self._request_response[schema_response_ref_name] = schema_ref_name
        return schema_ref_name


    def register_swagger_tag(self,
                             module_name,
                             name=None,
                             description=None):
        """Create or update a tags definition

        Args:
            - module_name (str): the blueprint or flask app name
            - name (str|None): the tag name
            - description (str|None): the tag descrition
        """
        tag = self._tags.get(module_name, {})
        if name:
            tag["name"] = name
        
        if description:
            tag["description"] = description
        self._tags[module_name] = tag


    def _extract_blueprints_information(self):
        """Extract the swagger tags and schemas defined in blueprints
        """
        for bp in self._app.blueprints:
            self._tags[bp] = self._extract_tags_from_blueprints(bp)
            self._extract_schemas_from_blueprints(bp)
        self.swagger_builder.register_swagger_tags(self._tags)

    
    def _extract_tags_from_blueprints(self, blueprint):
        """Get the blueprint tags from registered API

        Args:
            - blueprint (str): the blueprint

        Returns:
            - dict: the tag information
        """
        if isinstance(self._app.blueprints[blueprint], SwaggerFlaskBlueprint):
            return self._app.blueprints[blueprint].swagger_tag_spec
        
        tag = {"name": self.swagger_builder.transform_tag_name(blueprint)}
        return tag
    
    
    def _extract_schemas_from_blueprints(self, blueprint):
        """Get the schemas recorded in Swagger Blueprint and register 
        them in swagger components

        Args:
            - blueprint (str): the blueprint
        """
        schemas = None
        if isinstance(self._app.blueprints[blueprint], SwaggerFlaskBlueprint):
            schemas = self._app.blueprints[blueprint].swagger_schemas_modules
        
        for schema_module in schemas:
            schemas_cnts = [ schema for schema in dir(schema_module) if not schema.startswith("_") ]
            for schema_cnts in schemas_cnts:
                schema = getattr(schema_module, schema_cnts)
                schema_ref_name = self.swagger_builder.register_swagger_component_schema(schema)
                self._models[schema_ref_name] = self._models.get(schema_ref_name, {})

    
    def _extract_endpoint_information(self, endpoint):
        """Extract the endpoint information from header documentation

        Args:
            - endpoint (str): the function name related to specific endpoint

        Returns:
            - dict: the endpoint information
        """
        print(f"-------- {endpoint} ----------")
        endpoint_info = {}
        func_info = self._app.view_functions[endpoint].__doc__
        func_info = [content.strip() for content in func_info.split("\n\n")]
        func_info.reverse()

        endpoint_info["summary"] = func_info.pop()
        endpoint_info["parameters"] = []

        while func_info:
            endpoint_spec_group, spec_doc = func_info.pop().split(":", 1)
            endpoint_spec_group = endpoint_spec_group.strip()

            spec_doc_func, endpoint_info_tag = self.endpoint_docs_groups.get(endpoint_spec_group, (None, None))
            if spec_doc_func:
                params = spec_doc_func(spec_doc)
                if endpoint_info_tag == "parameters":
                    endpoint_info["parameters"] += params
                else:
                    endpoint_info[endpoint_info_tag] = params

        print(endpoint_info)
        print("\n")
        return endpoint_info


    def _extract_endpoint_path_params(self, params):
        """Extract the endpoint path parameters from function documentation

        Args:
            - params (str): the python function documentation related to path parameters

        Returns:
            - dict: the path parameters swagger specification
        """
        print("++++ Extract path parameters ++++")
        response = []
        f = StringIO(params)
        params_spec = yaml.safe_load(f)
        for param in params_spec:
            params_spec = self.swagger_builder.define_path_params(name=param.pop("name"),
                                                                  data_type=param.pop("type"),
                                                                  description=param.pop("description"),
                                                                  required=param.pop("required", True),
                                                                  additional_schema_rules=param)
            response.append(params_spec)
            
        return response
    

    def _extract_endpoint_description(self, params):
        """Extract the endpoint description from function documentation

        Args:
            - params (str): the python function documentation related to endpoint description

        Returns:
            - str: the description swagger specification
        """
        print("++++ Extract endpoint description ++++")
        response = params.strip()
        return response
    

    def _extract_endpoint_query_params(self, params):
        """Extract the endpoint query parameters from function documentation

        Args:
            - params (str): the python function documentation related to query parameters

        Returns:
            - dict: the query parameters swagger specification
        """
        print("++++ Extract query parameters ++++")
        response = []
        f = StringIO(params)
        params_spec = yaml.safe_load(f)
        for param in params_spec:
            param_spec = self.swagger_builder.define_query_params(name=param.pop("name"),
                                                                  data_type=param.pop("type"),
                                                                  description=param.pop("description"),
                                                                  allow_reserved=param.pop("allow_reserved", True),
                                                                  required=param.pop("required", True),
                                                                  additional_schema_rules=param)
            response.append(param_spec)
            
        return response
    

    def _extract_endpoint_custom_headers(self, params):
        """Extract the endpoint custom headers from function documentation

        Args:
            - params (str): the python function documentation related to custom headers

        Returns:
            - dict: the custom headers swagger specification
        """
        print("++++ Extract custom headers ++++")
        response = []
        f = StringIO(params)
        params_spec = yaml.safe_load(f)
        for param in params_spec:
            params_spec = self.swagger_builder.define_custom_headers(name=param.pop("name"),
                                                                     data_type=param.pop("type"),
                                                                     description=param.pop("description"),
                                                                     required=param.pop("required", True),
                                                                     additional_schema_rules=param)
            response.append(params_spec)
            
        return response
    

    def _extract_endpoint_request_bodies(self, params):
        """Extract the endpoint request bodies from function documentation

        Args:
            - params (str): the python function documentation related to request bodies

        Returns:
            - dict: the request bodies swagger specification
        """
        print("++++ Extract request bodies ++++")
        response = {}
        f = StringIO(params)
        params_spec = yaml.safe_load(f)
        for mimetype in params_spec:
            request_bodies = [self.swagger_builder._get_swagger_schema_ref(schema_id) 
                              for schema_id in params_spec[mimetype]["schemas"]]
            
            schema_bodies = self.swagger_builder.define_request_body_with_ref(mimetype,
                                                                              request_bodies,
                                                                              params_spec[mimetype].get("examples"))
            response = {
                **response,
                **schema_bodies
            }
        return response


    def _extract_endpoint_request_responses(self, params):
        """Extract the endpoint request responses from function documentation

        Args:
            - params (str): the python function documentation related to request responses

        Returns:
            - dict: the request responses swagger specification
        """
        print("++++ Extract responses ++++")
        response = {}
        f = StringIO(params)
        params_spec = yaml.safe_load(f)
        for status_code in params_spec:
            for mimetype in params_spec[status_code]["mime-types"]:
                request_responses = [self.swagger_builder._get_swagger_schema_ref(schema_id) 
                                     for schema_id in params_spec[status_code]["mime-types"][mimetype]["schemas"]]
            
                schema_responses = self.swagger_builder.define_request_response_with_ref(status_code,
                                                                                         mimetype,
                                                                                         request_responses,
                                                                                         params_spec[status_code].get("description"),
                                                                                         params_spec[status_code]["mime-types"][mimetype].get("examples"),
                                                                                         params_spec[status_code].get("headers"))
            
                response = {
                    **response,
                    **schema_responses
                }
        return response


    def _extract_endpoint_security(self, params):
        """Extract the endpoint security features from function documentation

        Args:
            - params (str): the python function documentation related to endpoint security

        Returns:
            - dict: the endpoint security swagger specification
        """
        print("++++ Extract endpoint security ++++")
        response = []
        f = StringIO(params)
        params_spec = yaml.safe_load(f)

        for security in params_spec:
            security_spec = self.swagger_builder.define_path_security(security)
            response.append(security_spec)

        return response


    def _extract_endpoints(self,
                           additional_methods=[]):
        """Extract the endpoints information defined in the functions header documentation

        Args:
            - additional_methods (list): the additional methods (OPTIONS, HEAD, ...) to persist
        """
        endpoints = [ endpoint for endpoint in self._app.url_map._rules_by_endpoint if endpoint != "static" ]
        response = {}
        methods_to_delete = {"OPTIONS", "HEAD"} - set(additional_methods)

        for endpoint in endpoints:

            endpoint_group = endpoint.split(".")
            tag = "Defaults"
            if len(endpoint_group) > 1:
                tag = self._tags[endpoint_group[0]]["name"]
            rule = self._app.url_map._rules_by_endpoint[endpoint][0]
            url_path = self._build_swagger_path_url(rule)
            operation_id = self.swagger_builder.transform_snake_to_lower_camel_case(endpoint_group[-1])
            endpoint_spec = response.get(url_path, {})
            endpoint_info = self._extract_endpoint_information(endpoint)

            methods = map(lambda method: method.lower(), (rule.methods - methods_to_delete))
            for method in methods:
                endpoint_spec = self._build_endpoint_spec_by_method(endpoint_info,
                                                                    method,
                                                                    endpoint_spec,
                                                                    tag,
                                                                    operation_id)
           
            response[url_path] = endpoint_spec
            
        self._endpoints = response


    def _build_endpoint_spec_by_method(self,
                                       endpoint_info,
                                       method,
                                       endpoint_spec,
                                       tag,
                                       operation_id):
        """Build endpoint specification by method

        Args:
            - endpoint_info (dict): the endpoint information
            - method (str): the endpoint method in lower case (get, post,...)
            - endpoint_spec (dict): the endpoint specifications
            - tag (str): the endpoint tag
            - operation_id (str): the endpoint identificators

        Returns:
            - dict: the endpoint the new method specification 
        """
        if method in ["get", "post", "put", "delete"]:
            endpoint_spec[method] = {
                **endpoint_info,
                "tags": [tag],
                "operation_id": operation_id
            }
        elif method == "options":
            endpoint_spec[method] = {
                "summary": "The CORS access",
                "description": "This endpoint is just only to know the CORS access",
                "parameters": endpoint_info["parameters"],
                "responses": self.swagger_builder.define_request_responses_options_method(),
                "tags": [tag],
                "operation_id": operation_id + "Option"
            }
        return endpoint_spec


    def _build_swagger_path_url(self, rule):
        """Build the url path based on the path parameters

        Args:
            - rule (Flask.Rule): the endpoint rule

        Returns:
            - str: the url in swagger format
        """
        path = ""
        for url_param, url_part in rule._trace[1:]:
            if url_param:
                path += '{%s}' % (url_part,)
            else:
                path += url_part
        return path

# JSRL Swagger - Library

This library is one of the multiple plugins of `jsrl_library_common` package, where you can generate the swagger documentation for your API in Python language

## Schemas

### Model schemas

By default the swagger package give you the following schemas:

- `HAL_SCHEMA`
- `HAL_SCHEMA_ERROR_MESSAGE`
- `HAL_SCHEMA_WITH_SINCE_PAGINATION`

### Security schemas

By default this library support the following security schemas:

- `DEFAULT_SECURITY_SCHEMAS`

## Library environment variables

In the following table you can see what are the expected environment variables that you must or can pass to library to customize the process

| Environment variable | Description |
| -------------------- | ----------- |
| JSRL_BASE_PATH       | Store the API base path (to can put in the links url prefix) |


## Models

This project brings the following classes to implement the swagger documentation in your Flask API

- `SwaggerFlaskBlueprint`: This class is inherited from `Blueprint` flask class and is used to group all endpoints defined itself in a specific tag.
- `FlaskSwagger`: This class extract the swagger information from Flask applications using the Blueprints and the controller functions documentations

### SwaggerFlaskBlueprint

As mentioned before this class overwrites the Blueprint class, therefore, the Blueprint logic doesn't change, but the new class has three new parameters when it is initialized in order to define the swagger tags and schemas, these are:

| Paramaters                | Type            | Description                                           |
| ------------------------- | --------------- | ----------------------------------------------------- |
| `swagger_tag_name`        | `str \| None`   | The name of the swagger tag related to this blueprint |
| `swagger_tag_description` | `str \| None`   | The description of swagger tag                        |
| `swagger_schemas_modules` | `list[Module]` | The swagger schemas modules                           |


### FlaskSwagger

As mentioned before this class extract the information from Flask application to can generate the swagger specifications. Also, to can specify the endpoints (swagger paths) definitions, this function extract the functions documentation and extract string sections to fill out the features like:

- Parameters
    - Path arguments
    - Query params
    - Custom headers
- Summary
- Description
- Request bodies
- Responses
- Security

## How to document?

### Create tag

For create a swagger tag, you can use the `SwaggerFlaskBlueprint` (Check class documentation)

**Example**

```py
from demo.schemas import hello_schemas
...
HELLO_RESOURCE = SwaggerFlaskBlueprint("hello_resource",
                                       __name__,
                                       swagger_tag_name="My Group",
                                       swagger_tag_description="Endpoints related to my first api with swagger implementation",
                                       swagger_schemas_modules=[hello_schemas])
...
```

### Define path summary

When you are documenting the controller function, the first line until double enter (\n\n), the swagger recognize those lines like endpoint or swagger path summary

**Example**

```py
@HELLO_RESOURCE.route("/say-hello",
                      methods=["GET"])
def say_hello():
    """Say hello when you call it

    ...
    """
```

**NOTE**: It's crucial in this part (when you are documenting a swagger path or endpoint) that the *separation lines* always **must be empty**. In the above example the *separation line* is the 5th line of code.

### Define path description

To define the endpoint or swagger path description, in the documentation of the function, a new section called `Long description` is created and end the description using double enter (\n\n)  

**Example**

```py
@HELLO_RESOURCE.route("/say-hello",
                      methods=["GET"])
def say_hello():
    """
    ...

    Long description:
    This endpoint return the hello message when this endpoint is requested

    ...
    """
```

**NOTE**: It's crucial in this part (when you are documenting a swagger path or endpoint) that the *separation lines* always **must be empty**. In the above example the *separation lines* are the 6th and 9th line of code.

### Define path arguments

When you have variables or arguments in your url path, in the documentation of the function, you have to define the structure data types, descriptions, and additional information about those arguments, for that you can use one of the following options (depending on your context):

#### Obligatory fields

```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Path arguments:
        - name: name
          type: string
          description: the name of user to say hello

    ...
    """
```

#### Basic configuration

```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Path arguments:
        - name: name
          type: string
          description: the name of user to say hello
          required: true

    ...
    """
```

#### Configuration with additional scheme rules

```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Path arguments:
        - name: name
          type: string
          description: the name of user to say hello
          required: true
          pattern: ^([A-Za-z]+)$

    ...
    """
```

#### Configuration with additional specifications

```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Path arguments:
        - name: name
          type: string
          description: the name of user to say hello
          required: true
          allowEmptyValue: true

    ...
    """
```

#### Configuration with examples

```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Path arguments:
        - name: name
          type: string
          description: the name of user to say hello
          required: true
          pattern: ^([A-Za-z]+)$
          examples:
            upperCamelCase:
                description: Name in upper camel case
                value: EDGAR
            lowerCamelCase:
                description: Name in lower camel case
                value: laura
            notAllowedValue:
                description: Not allow name
                value: laura01_

    ...
    """
```

**NOTE**: It's crucial in this part (when you are documenting a swagger path or endpoint) that the *separation lines* always **must be empty**.

### Define query parameters

When you want to use query parameters, in the documentation of the function, you have to define the structure data types, descriptions, and additional information about those arguments, for that you can use one of the following options (depending on your context):


#### Obligatory fields
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Query params:
        - name: age
          type: integer
          description: the age of user

    ...
    """
```

#### Basic configuration
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Query params:
        - name: age
          type: integer
          description: the age of user
          allow_reserved: true
          required: false

    ...
    """
```

#### Configuration with additional scheme rules
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Query params:
        - name: age
          type: integer
          description: the age of user
          allow_reserved: true
          required: false
          format: int32

    ...
    """
```

#### Configuration with additional specifications
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Query params:
        - name: age
          type: integer
          description: the age of user
          allow_reserved: true
          required: false
          allowEmptyValue: false

    ...
    """
```

#### Configuration with examples
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Query params:
        - name: age
          type: integer
          description: the age of user
          allow_reserved: true
          required: false
          examples:
            old:
              description: the old person
              value: 90
            young:
              description: the young person
              value: 20

    ...
    """
```

### Define custom headers

When you want to use custom headers, in the documentation of the function, you have to define the structure data types, descriptions, and additional information about those arguments, for that you can use one of the following options (depending on your context):

#### Obligatory fields
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Custom headers:
        - name: x-random-value
          type: string
          description: the random uuid

    ...
    """
```

#### Basic configuration
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Custom headers:
        - name: x-random-value
          type: string
          description: the random uuid
          required: true

    ...
    """
```


#### Configuration with additional scheme rules
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Custom headers:
        - name: x-random-value
          type: string
          description: the random uuid
          required: true
          format: uuid

    ...
    """
```

#### Configuration with additional specifications
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Custom headers:
        - name: x-random-value
          type: string
          description: the random uuid
          required: true
          allowEmptyValue: false

    ...
    """
```


#### Configuration with examples
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Custom headers:
        - name: x-random-value
          type: string
          description: the random uuid
          required: true
          examples:
            badStructure:
              description: bad value
              value: asdb
            expectedStructure:
              description: expected value
              value: 77e1c83b-7bb0-437b-bc50-a7a58e5660ac

    ...
    """
```

### Define request bodies

When you want to define request bodies, in the documentation of the function, you have to define the structure data types, and additional information about those arguments, for that you can use one of the following options (depending on your context)

**NOTE**: It important highlight that in this part the schemas must be registered in the blueprint and each value defined in the schemas list of request bodies documentation must be the attribute `$id` of the schema. Besides, for the schema name (`$id`) is recommended use in this scenario the prefix REQUEST, and its name must be alphabetic.

#### Obligatory fields
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Request bodies:
        application/json:
            schemas:
                - https://example.com/schemas/REQUESTPORTFOLIOGENERATEREPORT

    ...
    """
```

#### Configuration with examples
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Request bodies:
        application/json:
            schemas:
                - https://example.com/schemas/REQUESTHELLOUSERINFO
            examples:
                basicCase:
                    summary: Base case
                    value:
                        age: 1
                        nickname: "acme"
    ...
    """
```

### Define request responses

When you want to define request responses, in the documentation of the function, you have to define the structure data types, and additional information about those arguments, for that you can use one of the following options (depending on your context)

**NOTE**: It important highlight that in this part the schemas must be registered in the blueprint and each value defined in the schemas list of request bodies documentation must be the attribute `$id` of the schema. Besides, for the schema name (`$id`) is recommended use in this scenario the prefix RESPONSE, and its name must be alphabetic.

#### Complete examples
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Request responses:
        200:
            description: The salutation was generated successfully
            headers:
                Access-Control-Allow-Origin:
                    schema:
                        type: "string"
            mime-types:
                application/json:
                    schemas:
                        - https://example.com/schemas/RESPONSEHELLOUSERINFO

    ...
    """
```

### Define security features

When you want to define x-api-key and Authorization attributes, you can use the following specification where:

- `api-key`: Define that you API required a `x-api-key` attribute in headers
- `swagger-authorization`: Define that this specific endpoint required the `Authorization` attributes and the list of elements related to this attribute are the scopes expected in the access token.

#### Complete examples
```py
@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello():
    """
    ...

    Security:
        - api-key
        - swagger-authorization:
            - demo/internal

    ...
    """
```


## Tutorial 

Let's start with a simple API.

That is the directory structure that we are working in this tutorial
```
.
 ┗ 📂 demo
   ┣ 📜 app.py
   ┣ 📜 build_swagger.py
   ┣ 📂 resource
   ┃ ┗ 📜 hello_controller.py
   ┗ 📂 schemas
     ┗ 📜 hello_schemas.py
```

### app.py

The app file create the Flask application, to run the HTTP Backend server.

Copy and paste the content of `app.py` file

```py
from demo.resource.hello_controller import HELLO_RESOURCE

APP = app = Flask(__name__)
APP.register_blueprint(HELLO_RESOURCE)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port="8080")
```

### hello_controller.py

In this file we have a tangible example of how to document a simple API with this tool.

First, we create the blueprint called `hello_resource` in the constant `HELLO_RESOURCE` and defined the name of *swagger tag* and *the tag description*

```py
from jsrl_library_common.models.swagger.flask_swagger_blueprint import SwaggerFlaskBlueprint

HELLO_RESOURCE = SwaggerFlaskBlueprint("hello_resource",
                                       __name__,
                                       swagger_tag_name="My Group",
                                       swagger_tag_description="Endpoints related to my first api with swagger implementation")


@HELLO_RESOURCE.route("/say-hello",
                      methods=["GET"])
def say_hello():
    """Say hello when you call it

    Long description:
    This endpoint return the hello message when this endpoint is requested

    ...
    """
    return "Hello, World!"


@HELLO_RESOURCE.route("/say-hello/<string:name>",
                      methods=["GET"])
def say_hello(name):
    """Say hello to specific name

    Path arguments:
        - name: name
          type: string
          description: the name of user to say hello
          required: true
          pattern: ^([A-Za-z]+)$
          examples:
            upperCamelCase:
                description: Name in upper camel case
                value: EDGAR
            lowerCamelCase:
                description: Name in lower camel case
                value: laura
            notAllowedValue:
                description: Not allow name
                value: laura01_

    ...
    """
    return f"Hello {name}"
```




###
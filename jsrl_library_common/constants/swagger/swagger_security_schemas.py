DEFAULT_SECURITY_SCHEMAS = {
    "api-key": {
        "type": "apiKey",
        "in": "header",
        "name": "x-api-key",
        "description": "The API Gateway api key"
    },
    "swagger-authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "The access token"
    }
}
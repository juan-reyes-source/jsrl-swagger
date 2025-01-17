HAL_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/schemas/HALFORMAT",
    "type": "object",
    "properties": {
        "_embedded": {
            "type": "object"
        },
        "_links": {
            "type": "object",
            "properties": {
                "self": {
                    "type": "string"
                }
            },
            "required": [
                "self"
            ]
        }
    },
    "required": [
        "_embedded",
        "_links"
    ],
    "additionalProperties": False
}


HAL_SCHEMA_WITH_SINCE_PAGINATION = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/schemas/HALSCHEMAWITHSINCEPAGINATION",
    "allOf": [
        {
            "$ref": "/schemas/HALFORMAT"
        }
    ],
    "properties": {
        "_links": {
            "properties": {
                "next": {
                    "type": "string"
                }
            }
        }
    }
}


HAL_SCHEMA_ERROR_MESSAGE = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/schemas/HALFORMATERRORMESSAGE",
    "allOf": [
        {
            "$ref": "/schemas/HALFORMAT"
        }
    ],
    "properties": {
        "_embedded": {
            "properties": {
                "message": {
                    "type": "string"
                }
            }
        }
    }
}

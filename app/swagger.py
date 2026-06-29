from config import BASE_URL


OPENAPI_SPEC = {
    'openapi': '3.0.3',
    'info': {
        'title': 'E-commerce Store API',
        'version': '1.0.0',
        'description': 'Simple Flask REST API for an e-commerce store.',
    },
    'servers': [
        {
            'url': BASE_URL,
            'description': 'Local development server',
        }
    ],
    'paths': {
        '/health': {
            'get': {
                'summary': 'Check API health',
                'responses': {
                    '200': {
                        'description': 'API is running',
                    }
                },
            }
        },
        '/goods': {
            'get': {
                'summary': 'Get all goods',
                'responses': {
                    '200': {
                        'description': 'List of goods',
                    }
                },
            },
            'post': {
                'summary': 'Create a good',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/GoodCreate'
                            }
                        }
                    },
                },
                'responses': {
                    '201': {
                        'description': 'Good created',
                    },
                    '400': {
                        'description': 'Validation error or duplicate good',
                    },
                    '404': {
                        'description': 'Category not found',
                    },
                },
            },
        },
        '/goods/{good_id}': {
            'get': {
                'summary': 'Get a good by id',
                'parameters': [
                    {
                        '$ref': '#/components/parameters/GoodId'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Good found',
                    },
                    '404': {
                        'description': 'Good not found',
                    },
                },
            },
            'put': {
                'summary': 'Update a good',
                'parameters': [
                    {
                        '$ref': '#/components/parameters/GoodId'
                    }
                ],
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/GoodCreate'
                            }
                        }
                    },
                },
                'responses': {
                    '200': {
                        'description': 'Good updated',
                    },
                    '400': {
                        'description': 'Validation error',
                    },
                    '404': {
                        'description': 'Good or category not found',
                    },
                },
            },
            'delete': {
                'summary': 'Delete a good',
                'parameters': [
                    {
                        '$ref': '#/components/parameters/GoodId'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Good deleted',
                    },
                    '404': {
                        'description': 'Good not found',
                    },
                },
            },
        },
        '/categories': {
            'get': {
                'summary': 'Get all categories',
                'responses': {
                    '200': {
                        'description': 'List of categories',
                    }
                },
            },
            'post': {
                'summary': 'Create a category',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/CategoryCreate'
                            }
                        }
                    },
                },
                'responses': {
                    '201': {
                        'description': 'Category created',
                    },
                    '400': {
                        'description': 'Validation error or duplicate category',
                    },
                },
            },
        },
        '/categories/{category_id}/goods': {
            'get': {
                'summary': 'Get goods by category',
                'parameters': [
                    {
                        '$ref': '#/components/parameters/CategoryId'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'List of goods by category',
                    },
                    '404': {
                        'description': 'Category not found',
                    },
                },
            }
        },
    },
    'components': {
        'parameters': {
            'GoodId': {
                'name': 'good_id',
                'in': 'path',
                'required': True,
                'schema': {
                    'type': 'integer'
                },
            },
            'CategoryId': {
                'name': 'category_id',
                'in': 'path',
                'required': True,
                'schema': {
                    'type': 'integer'
                },
            },
        },
        'schemas': {
            'Good': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'integer',
                        'example': 1,
                    },
                    'name': {
                        'type': 'string',
                        'example': 'Phone',
                    },
                    'price': {
                        'type': 'number',
                        'example': 500.0,
                    },
                    'category_id': {
                        'type': 'integer',
                        'example': 3,
                    },
                },
            },
            'GoodCreate': {
                'type': 'object',
                'required': [
                    'name',
                    'price',
                    'category_id',
                ],
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Phone',
                    },
                    'price': {
                        'type': 'number',
                        'example': 500,
                    },
                    'category_id': {
                        'type': 'integer',
                        'example': 3,
                    },
                },
            },
            'Category': {
                'type': 'object',
                'properties': {
                    'category_id': {
                        'type': 'integer',
                        'example': 3,
                    },
                    'name': {
                        'type': 'string',
                        'example': 'Phones',
                    },
                },
            },
            'CategoryCreate': {
                'type': 'object',
                'required': [
                    'name',
                ],
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Laptops',
                    },
                },
            },
        },
    },
}

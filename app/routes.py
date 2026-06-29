import logging

from flask import Flask, Response, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from config import HOST, PORT
from logger_config import setup_logging
from models import (
    add_category,
    add_good,
    delete_good_by_id,
    get_all_categories,
    get_all_goods,
    get_all_goods_by_category,
    get_category_by_id,
    get_good_by_id,
    init_db,
    update_good_by_id,
)
from schemas import CategorySchema, GoodSchema
from swagger import OPENAPI_SPEC

setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

good_schema = GoodSchema()
goods_schema = GoodSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class Goods(Resource):
    def get(self):
        goods = get_all_goods()
        logger.info('GET /goods returned %s goods', len(goods))
        return goods_schema.dump(goods), 200

    def post(self):
        try:
            good = good_schema.load(request.json)
        except ValidationError as error:
            logger.warning('POST /goods validation error: %s', error.messages)
            return error.messages, 400

        if get_category_by_id(good.category_id) is None:
            logger.warning(
                'POST /goods failed, category not found: id=%s',
                good.category_id
            )
            return {'message': 'Category not found'}, 404

        created_good = add_good(good)

        if created_good is None:
            logger.warning('POST /goods failed, duplicate name: %s', good.name)
            return {'message': 'Good with this name already exists'}, 400

        logger.info('POST /goods created good: id=%s', created_good.id)
        return good_schema.dump(created_good), 201


class GoodDetail(Resource):
    def get(self, good_id: int):
        good = get_good_by_id(good_id)

        if good is None:
            logger.warning('GET /goods/%s failed, good not found', good_id)
            return {'message': 'Good not found'}, 404

        logger.info('GET /goods/%s returned good', good_id)
        return good_schema.dump(good), 200

    def put(self, good_id: int):
        try:
            good = good_schema.load(request.json)
        except ValidationError as error:
            logger.warning(
                'PUT /goods/%s validation error: %s',
                good_id,
                error.messages
            )
            return error.messages, 400

        if get_category_by_id(good.category_id) is None:
            logger.warning(
                'PUT /goods/%s failed, category not found: id=%s',
                good_id,
                good.category_id
            )
            return {'message': 'Category not found'}, 404

        updated_good = update_good_by_id(good_id, good)

        if updated_good is None:
            logger.warning('PUT /goods/%s failed, good not found', good_id)
            return {'message': 'Good not found'}, 404

        logger.info('PUT /goods/%s updated good', good_id)
        return good_schema.dump(updated_good), 200

    def delete(self, good_id: int):
        is_deleted = delete_good_by_id(good_id)

        if not is_deleted:
            logger.warning('DELETE /goods/%s failed, good not found', good_id)
            return {'message': 'Good not found'}, 404

        logger.info('DELETE /goods/%s deleted good', good_id)
        return {'message': 'Good deleted'}, 200


class Categories(Resource):
    def get(self):
        categories = get_all_categories()
        logger.info('GET /categories returned %s categories', len(categories))
        return categories_schema.dump(categories), 200

    def post(self):
        try:
            category = category_schema.load(request.json)
        except ValidationError as error:
            logger.warning(
                'POST /categories validation error: %s',
                error.messages
            )
            return error.messages, 400

        created_category = add_category(category)

        if created_category is None:
            logger.warning(
                'POST /categories failed, duplicate name: %s',
                category.name
            )
            return {'message': 'Category with this name already exists'}, 400

        logger.info(
            'POST /categories created category: id=%s',
            created_category.category_id
        )
        return category_schema.dump(created_category), 201


class CategoryGoods(Resource):
    def get(self, category_id: int):
        if get_category_by_id(category_id) is None:
            logger.warning(
                'GET /categories/%s/goods failed, category not found',
                category_id
            )
            return {'message': 'Category not found'}, 404

        goods = get_all_goods_by_category(category_id)
        logger.info(
            'GET /categories/%s/goods returned %s goods',
            category_id,
            len(goods)
        )
        return goods_schema.dump(goods), 200

class Health(Resource):
    def get(self):
        logger.info('GET /health returned ok')
        return {'status': 'ok'}, 200


class OpenApiSpec(Resource):
    def get(self):
        logger.info('GET /openapi.json returned swagger spec')
        return OPENAPI_SPEC, 200


class SwaggerDocs(Resource):
    def get(self):
        logger.info('GET /docs returned swagger ui')
        html = '''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>E-commerce Store API Docs</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
                SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui'
                });
            </script>
        </body>
        </html>
        '''
        return Response(html, mimetype='text/html')


api.add_resource(Goods, '/goods')
api.add_resource(GoodDetail, '/goods/<int:good_id>')
api.add_resource(Categories, '/categories')
api.add_resource(CategoryGoods, '/categories/<int:category_id>/goods')
api.add_resource(Health, '/', '/health')
api.add_resource(OpenApiSpec, '/openapi.json')
api.add_resource(SwaggerDocs, '/docs')


if __name__ == '__main__':
    init_db()
    app.run(host=HOST, port=PORT, debug=True)

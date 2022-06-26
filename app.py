import re

from flask import Flask, request

from product_repository import insert_products, get_product, get_children, delete_product, update

app = Flask(__name__)


def validation_error():
    return {
               "code": 400,
               "message": "Validation Failed"
           }, 400


def item_not_found_error():
    return {
               "code": 404,
               "message": "Item not found"
           }, 404


@app.post('/imports')
def imports():
    body = request.get_json()
    products = [
        (item["id"], item["name"], item["parentId"], item.get("price"), item["type"], body["updateDate"])
        for item in body["items"]
    ]
    for item in body["items"]:
        parent = get_product(item["parentId"])
        if parent:
            update(parent[2], body["updateDate"])
            update(item["parentId"],  body["updateDate"])

    insert_products(products)
    print(products)
    return "OK"


def nodes(product_id):
    if re.match(r'^[\da-fA-F]{8}\b-[\da-fA-F]{4}\b-[\da-fA-F]{4}\b-[\da-fA-F]{4}\b-[\da-fA-F]{12}$', product_id)\
            is None:
        return validation_error()

    product = get_product(product_id)
    if product is None:
        return {
                   "code": 404,
                   "message": "Item not found"
               }, 404

    children = get_children(product[0])
    result = {"id": product[0], "name": product[1], "parentId": product[2], "price": product[3], "type": product[4],
              "date": product[5]}
    if len(children) > 0:
        result["children"] = [nodes(child[0]) for child in children]
    else:
        result["children"] = None

    return result


@app.get('/nodes/<product_id>')
def get_nodes(product_id):
    result = nodes(product_id)
    try:
        if result[0]["code"] == 404:
            return {
                       "code": 404,
                       "message": "Item not found"
                    }, 404
    except KeyError:
        get_price(result)
        return result

def get_price(res):
    if res["type"] == "OFFER":
        return res["price"], 1
    sum = 0
    counts = 0
    for child in res["children"]:
        price, count = get_price(child)
        sum += price
        counts += count

    res["price"] = sum // counts

    return sum, counts


@app.delete('/delete/<product_id>')
def delete(product_id):
    if re.match(r'^[\da-fA-F]{8}\b-[\da-fA-F]{4}\b-[\da-fA-F]{4}\b-[\da-fA-F]{4}\b-[\da-fA-F]{12}$', product_id)\
            is None:
        return validation_error()

    product = get_product(product_id)
    if product is None:
        return item_not_found_error()

    children = get_children(product_id)
    delete_product(product_id)
    for child in children:
        delete(child[0])
    return "OK"


@app.get('/sales')
def sales():
    return "OK"

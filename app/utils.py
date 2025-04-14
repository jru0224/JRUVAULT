import json

def load_products():
    with open('products.json', encoding='utf-8') as f:
        return json.load(f)

def save_products(products):
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def get_next_product_id(products):
    return max([p['id'] for p in products], default=0) + 1

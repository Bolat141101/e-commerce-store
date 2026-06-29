import sys

sys.path.append('app')

from app.models import get_all_goods, init_db, seed_default_goods


if __name__ == '__main__':
    init_db()
    created_count = seed_default_goods()
    goods = get_all_goods()

    print(f'Created goods: {created_count}')
    print(f'Total goods: {len(goods)}')

    for good in goods:
        print(good)

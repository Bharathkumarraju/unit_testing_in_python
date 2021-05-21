import csv

import pytest

from gilded_rose import Item, GildedRose


def read_items():
    cases = []
    with open("items.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            sell_in = int(row['sell_in'])
            quality = int(row['quality'])
            expected_sell_in = int(row['expected_sell_in'])
            expected_quality = int(row['expected_quality'])

            case = (name, sell_in, quality, expected_sell_in, expected_quality)
            cases.append(case)
    return cases


@pytest.mark.parametrize("name, sell_in, quality, expected_sell_in, expected_quality",
                         read_items())
def test_update_items(name, sell_in, quality, expected_sell_in, expected_quality):
    item = Item(name, sell_in, quality)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality

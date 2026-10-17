import pytest
from fastapi import HTTPException

import main
from main import Item


def test_item_defaults():
    item = Item()
    assert item.text is None
    assert item.is_done is False


def test_root():
    assert main.root() == {"Hello": "World"}


def test_create_item_appends_and_returns_all_items():
    first = Item(text="first")
    second = Item(text="second", is_done=True)

    assert main.create_item(first) == [first]
    assert main.create_item(second) == [first, second]
    assert main.items == [first, second]


def test_list_items_empty():
    assert main.list_items() == []


def test_list_items_default_limit_is_10():
    for i in range(15):
        main.create_item(Item(text=str(i)))

    result = main.list_items()

    assert len(result) == 10
    assert [item.text for item in result] == [str(i) for i in range(10)]


def test_list_items_custom_limit():
    for i in range(5):
        main.create_item(Item(text=str(i)))

    assert [item.text for item in main.list_items(limit=3)] == ["0", "1", "2"]


def test_get_item_returns_item_by_index():
    apple = Item(text="apple")
    main.create_item(apple)

    assert main.get_item(0) is apple


def test_get_item_out_of_range_raises_404():
    with pytest.raises(HTTPException) as exc_info:
        main.get_item(0)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item 0 not found"


def test_get_item_negative_id_raises_404():
    main.create_item(Item(text="apple"))

    with pytest.raises(HTTPException) as exc_info:
        main.get_item(-1)

    assert exc_info.value.status_code == 404

def validate_feed_data(feed_data: dict):
    _validate_feed_data(feed_data)

    for item_data in feed_data["items_data"]:
        _validate_item_data(item_data)


def _validate_feed_data(feed_data):
    for required in ["feed_language", "feed_name", "items_data"]:
        if required not in feed_data:
            raise ValueError(
                f"feed_data must contain {required}. feed_data is {feed_data}"
            )


def _validate_item_data(item_data):
    for required in ["link", "description"]:
        if required not in item_data:
            raise ValueError(
                f"item_data must contain {required}. item_data is {item_data}"
            )

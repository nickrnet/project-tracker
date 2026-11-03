import uuid


def handle_uuid_list(list_to_validate_with, uuid_list):
    valid_uuids = []
    for item_id in uuid_list:
        try:
            item_id = uuid.UUID(item_id)
            if item_id in list_to_validate_with:
                valid_uuids.append(item_id)
        except ValueError:
            continue
    return valid_uuids

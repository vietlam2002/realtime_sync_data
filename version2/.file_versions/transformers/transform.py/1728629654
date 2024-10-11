from typing import Dict, List

# Block transform để xử lý dữ liệu
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(messages: List[Dict], *args, **kwargs):
    """
    Transformer block to process Kafka messages and prepare for export to PostgreSQL.

    Args:
        messages: List of messages in the stream.

    Returns:
        List of dictionaries representing rows to be inserted into PostgreSQL.
    """
    transformed_records = []

    for message in messages:
        operation = message.get('payload', {}).get('op')
        after_data = message.get('payload', {}).get('after')
        before_data = message.get('payload', {}).get('before')

        if operation in ['c', 'u'] and after_data:  # Create or update
            record = {
                'id': after_data["id"],
                'first_name': after_data["first_name"],
                'last_name': after_data["last_name"],
                'email': after_data["email"]
            }
            transformed_records.append(record)
        elif operation == 'd' and before_data:  # Delete
            record = {
                'id': before_data["id"],  # Use the ID for delete operation
                '_operation': 'delete'  # Optional flag for exporter to handle deletions
            }
            transformed_records.append(record)

    return transformed_records

from django.db import models


def code_in_string(id, head, size=7):
    result = head
    for _ in range(size - len(head) - len(str(id))):
        result += '0'
    result += str(id)
    return result

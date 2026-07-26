def recoder_students(L):
    slow = L
    fast = l
    while fast.next is not None and fast.next.next is not None:
        fast = fast.next.next
        slow = slow.next

    second_head = slow.next
    slow.next = None

    return secode_head



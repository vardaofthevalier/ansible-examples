# return the length of a list
def length(lst):
    return len(lst)


# append an item to a list
def append(lst, item):
    lst.append(item)
    return lst


# combine two lists
def extend(lst1, lst2):
    lst1.extend(lst2)
    return lst1


# return whether or not a list contains a particular item
def contains(lst, item):
    return item in lst


# remove an object from a list given an attribute to key on
def remove(lst, item, key=None):
    for i, l in enumerate(lst):
        if key is not None and l[key] == item:
            lst.pop(i)
        elif l == item:
            lst.pop(i)

    return lst


# get the intersection of two lists of objects given an attribute
def intersection_by_key(original, intersection, key=None):
    return filter(lambda x: x[key] in intersection, original)
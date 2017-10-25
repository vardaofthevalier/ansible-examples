# return the keys of a dictionary
def keys(dictionary):
    return dictionary.keys()


# return the values of a dictionary
def values(dictionary):
    return dictionary.values()


# return the string representation of a dictionary
def dict_to_string(d):
    return str(d)


# merge two dictionaries
def merge(d1, d2):
    for k, v in d2.iteritems():
        if k in d1.keys():
            if type(v) is dict:
                if type(d1[k]) is dict:
                    merge(d1[k], v)

                elif d1[k] == 'none' or d1[k] is None:
                    d1[k] = v

                else:
                    n = [v, d1[k]]
                    d1[k] = n

            elif type(v) is list:
                if type(d1[k]) is list:
                    d1[k].extend(v)

                elif d1[k] == 'none' or d1[k] is None:
                    d1[k] = v

                else:
                    n = [v, d1[k]]
                    d1[k] = n

            elif v == 'none' or v is None:
                pass

            else:
                n = [v, d1[k]]
                d1[k] = n
        else:
            d1.update({
                k: v
            })

    return d1
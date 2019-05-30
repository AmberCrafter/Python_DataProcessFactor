def flatten(multi_list):
    flatten = lambda x: [subitem for item in x for subitem in flatten(item)] \
            if type(x) is list else [x]  
    return flatten(multi_list)
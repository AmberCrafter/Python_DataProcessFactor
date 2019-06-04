def flatten(multi_list):
    flatten = lambda x: [subitem for item in x for subitem in flatten(item)] \
            if type(x) is list else [x]  
    return flatten(multi_list)

if __name__ == "__main__":
    a=["1",[1,[2,23]],3,["asd",["123"]]]
    print(flatten(a))

def write_image(img_obj,path):

    with open(path,'wb') as fp:
        for i in img_obj.chunks():
            fp.write(i)




def split_list(list1,groupsize):

    ret_list = []
    tem_l = []
    for l in list1:
        tem_l.append(l)
        if len(tem_l)==groupsize:
            ret_list.append(tem_l)
            tem_l=[]
    ret_list.append(tem_l)
    return ret_list

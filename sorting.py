import random

a=int(input("enter the size of your liste:"))
list=[]
for i in range(1,a):
    list.append(i)
print(list)
random.shuffle(list)
print(list)

#tri par selection
def select_sort(list):
    for j in range(len(list)):
        for i in range(j,len(list)):
            if list[i]<list[j]:
                list[i],list[j]=list[j],list[i]
    return list

def bubble_sort(list):
    boolean=False
    while boolean==False:
        a=0
        for i in range(len(list)-1) :
            if list[i]>list[i+1]:
                list[i],list[i+1]=list[i+1],list[i]
                print(list)
                a-=1
            else:
                a+=1
            if a==len(list)-1:
                boolean=True
    return list
bubble_sort(list)
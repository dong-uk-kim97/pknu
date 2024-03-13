a = [7,2,1,8,9,10]
# max함수 쓰지 않고 max값 구하기
max = 0
for i in a:
    if i>max:
        max=i
    else:continue
print(max)

# 최댓값과 그 전 값 구하기
for i in range(len(a)-1):
    if a[i]>a[i+1]:
        a[i+1]=a[i]
    else:
        continue
print(a[4],a[5])

for i in range(len(a)-1):
    if a[i]>a[i+1]:
        a[i],a[i+1] = a[i+1],a[i]
    else:
        continue
print(a[4],a[5])

# 알파벳 순서대로 만들기
a = ['a','a','c','b','D','E']

for i in range(len(a)):
    if a[i]=='a':
        a[0]='a'
    elif a[i]=='b':
        a[1]='b'
    elif a[i]=='c':
        a[2]='c'
    elif a[i]=='D':
        a[3]='D'
    elif a[i]=='E':
        a[4]='E'
a.pop(5)
print(a)

for i in range(len(a)):
    if i==0:
        a[i]=='a'
    elif i==1:
        a[i]='b'
    elif i==2:
        a[i]='c'
    elif i==3:
        a[i]='D'
    elif i==4:
        a[i]='E'
    elif i==5:
        a.pop(i)
print(a)


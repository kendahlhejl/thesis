def decdeg2dms(dd):
    mult = -1 if dd < 0 else 1
    mnt,sec = divmod(abs(dd)*3600, 60)
    deg,mnt = divmod(mnt, 60)
    return mult*deg, mult*mnt, mult*sec

# negative value returns all negative elements

list = ['36.669882170563', '-85.435551987099', '54.643555369017']

input = float(list[1])
print(decdeg2dms(input))
from string import maketrans

value = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."

subs1 = "abcdefghijklmnopqrstuvwxyz"
subs2 = "yzabcdefghijklmnopqrstuvwx"
# trans = string.maketrans(subs2, subs2)

trantab = maketrans(subs2, subs1)

print("map".translate(trantab))


#
# result = ''
# for ch in value:
#     if ch in subs2:
#         index = subs2.find(ch)
#         ch = subs1[index]
#
#     result += ch
#
# print(result)
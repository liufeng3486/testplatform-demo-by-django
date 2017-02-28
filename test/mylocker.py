a = '''orderCode	dealCode	paymentServiceCode	description	merchantOrderNo	merchantOrderName	orderSequence	paymentChannel	orderAmount	paymentAmount	currency	transactionSequence	transactionTime	refRefundSequence	refReverseSequence
'''
b = a.split("	")
for i in b:
    print  "item.set%s(request.getParameter(\"%s\"));"%(i[0].upper()+i[1:],i)


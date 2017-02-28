a = '''
    item.setOrderCode(request.getParameter("orderCode"));
    item.setDealCode(request.getParameter("dealCode"));
    item.setPaymentServiceCode(request.getParameter("paymentServiceCode"));
    item.setDescription(request.getParameter("description"));
    item.setMerchantOrderNo(request.getParameter("merchantOrderNo"));
    item.setMerchantOrderName(request.getParameter("merchantOrderName"));
    item.setOrderSequence(request.getParameter("orderSequence"));
    item.setPaymentChannel(request.getParameter("paymentChannel"));
//    item.setOrderAmount(Long.parseLong(request.getParameter("orderAmount")));
//    item.setPaymentAmount(Long.parseLong(request.getParameter("paymentAmount")));

    if (request.getParameter("orderAmount")!=""&&request.getParameter("orderAmount")!= null){
        item.setOrderAmount(Long.parseLong(request.getParameter("orderAmount")));
    }
    if (request.getParameter("paymentAmount")!=""&&request.getParameter("paymentAmount")!=null){
        item.setPaymentAmount(Long.parseLong(request.getParameter("paymentAmount")));
    }
    item.setCurrency(request.getParameter("currency"));
    item.setTransactionSequence(request.getParameter("transactionSequence"));
    item.setTransactionTime(request.getParameter("transactionTime"));
    item.setRefundSequence(request.getParameter("refRefundSequence"));
    item.setReverseSequence(request.getParameter("refReverseSequence"));

'''
import re
temp = 'out.println(" <tr><td>replace<input align=\\"left\\" type=\\"text\\" name=\\"replace\\" id=\\"replace\\" value=\\""+String.valueOf(result.getreplace())+"\\"></td></tr>");'
d = re.findall("set(.*)\(",a)
for i in d:
    print i
    # temp_2 = temp.replace("replace",i)
    # print temp_2


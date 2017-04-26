# coding: utf-8

# # define functions -get stock data, create datatable and dataset -

from bs4 import BeautifulSoup
import requests
import re
import numpy as np

def get_rawdata():
    # get html data from google
    url1 = 'https://www.google.com/finance/historical?q='
    url2 = raw_input(' Please input stock name : ')
    url3 = '&start=0&num=200'
    url = url1 + url2 + url3
    html_data = requests.get(url)
    string_data_tmp = html_data.content
    string_data = string_data_tmp.replace(',','') 

    check_patterns = 'prices'
    if re.search(check_patterns, string_data):
        print ''
        print ' We got stock data ! '
        print ' Now data processing are woking.  Please wait a while...'
        print ''
        
        # create soup object
        soup_object = BeautifulSoup(string_data, 'html.parser')
        
        # find div's class and id and extract tr_data from tables
        summary = soup_object.find("div", {'class':'gf-table-wrapper sfe-break-bottom-16','id':"prices"})
        tables = summary.find_all('table')
        tr_data = tables[0].find_all('tr')
        
        # extract td data from tr data and stored data list.
        rawdata_list = []
        for tr in tr_data:
            td_data = tr.find_all('td')
            for td in td_data:
                text = td.find(text=True) 
                rawdata_list.append(text)   
        print 'OK,  Please continue.'   
        print ''
        return rawdata_list
    
    else:
        print ''
        print ' Sorry ! There is no stock data.  Please try again.'
        print ''


# create datatable table from rawdata
# rawdata has 1200 rows (6 vectors * 200 days )
# n: number of row
import csv

def create_datatable(rawdata):
    try:
        open_list=[]; high_list =[]; low_list=[]; close_list=[]; volume_list=[]
        list_names = [open_list, high_list, low_list, close_list, volume_list]
        n =1200
        for i, item in enumerate(list_names):
            i = i +1
            while i < n: item.append(float(rawdata[i]));i = i + 6;

        stock_data_list =[]
        for i in list_names:
            stock_data_list.append(i)
        datatable_tmp = np.array(stock_data_list).astype('float')
        datatable = datatable_tmp.T
        
        file_write = raw_input('Would you like to save datatable ?  If Yes, please Enter or y : ')
        if file_write == 'y' or file_write == '':
            f = open('datatable.csv', 'w')
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(datatable)
            f.close()
        
        #print 'Table shape is : ', datatable.shape
        #np.savetxt("stockdata.csv", datatable, fmt="%.09f",delimiter=",")
        return datatable
    
    except ValueError as v:
        print 'Sorry !  Some data are Not a number.  The error message is',v
        print 'Please try again.'



# create training set (feature vector and label data) from datatable

# calculate difference of daily up and down
# a: high price
# b: low price
# c: stock price today
# d: stock price  yersterday
# e: volume today
# f: volume  yersterday
# g: stock price tommorow
# n: number of row

def create_dataset(datatable):
    # create feature vector
    daytime_diff=[]; day_diff=[]; volume_diff=[]
    n = 199
    for i in range(n):
        a=datatable[i,1]
        b=datatable[i,2]
        c=datatable[i,3]
        d=datatable[i+1,3]
        e=datatable[i,4]
        f=datatable[i+1,4]
        daytime_diff.append((a - b)/c)
        day_diff.append((c - d)/c)
        volume_diff.append((e -f)/e)

    feature_vector_list =[]
    feature_vector_list.append(daytime_diff[1:n])
    feature_vector_list.append(day_diff[1:n]) 
    feature_vector_list.append(volume_diff[1:n])

    fvector_train_tmp = np.array(feature_vector_list)
    fvector_train = fvector_train_tmp.T
    #print 'Feature dataset shape is : ', fvector_train.shape

    # create label
    label_updown=[];
    for i in range(n):
        c=datatable[i,3]
        g=datatable[i-1,3]
        if g-c>0:
            label_updown.append(1)
        else:
            label_updown.append(-1)            
    label_train = np.array([]).astype('int');
    for i in range(1,n):
        c=datatable[i,3]
        g=datatable[i-1,3]
        if g-c>0:
            label_train = np.append(label_train, 1);
        else:
            label_train = np.append(label_train, -1);
    #print  'Label dataset shape is : ',label_train.shape
    
    return fvector_train, label_train


# # Building Model


import sklearn
from sklearn.linear_model import LinearRegression
#  X: three feature vector
#  Y: label
model = LinearRegression()


# # define functions - apply model and calculate  accuracy -


# create apply to model functions
# input present stock data and then print tomorrow's stock price is up or down
# present_data: lateset data

def apply_model(present_data):
    answer = model.predict(present_data)
    if answer > 0:
        print ''
        print "This stock will be going up tommorow.  Buy it !"
    else:
        print "This stock will be going down.  Don't buy it ! "



# create calculate  Accuracy function

# If value is more than 0, it is changed to 1 and save "analize_result".
# 1 means that stock value will be up
# -1 means that stock value will be down

def cal_accuracy(answer_list, actual_list):
    analize_result = np.array([]);
    for i in answer_list:
        if i > 0:
            analize_result  = np.append(analize_result, 1);
        else :
            analize_result  = np.append(analize_result, -1); 
    # just check
    #print (analize_result[0:10]);

    count_correct = 0.0
    count_wrong =0.0
    for r, c in enumerate(analize_result):
        if c == actual_list[r]:
            count_correct += 1;
        else:
            count_wrong +=1;
    #print "The number of correct is : ", count_correct;
    #print "The number of wrong is : ", count_wrong;
    accuracy = count_correct/(count_correct+count_wrong)*100
    print "The accuracy is :  %0.1f"%accuracy, "%"


# # Apply to Model
# main #
print ''
print '/----------------------------------------------------------/'
print '   Welcome to simple stock predictive program'
print '/----------------------------------------------------------/'
print ''

while True:
    print ''
    user_continue = raw_input('Would you like to continue ?  Press enter or y to continue : ')
    if user_continue == 'y' or user_continue =='':
        
        rawdata = get_rawdata()                # step1
        datatable = create_datatable(rawdata)  # step2
        X, Y = create_dataset(datatable)       # step3
        model.fit(X,Y)                         # step4
        Z = model.predict(X)
        apply_model(X[0].reshape(1,-1))        # step5
        cal_accuracy(Z, Y)
    else:
        break

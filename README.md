1. This code is stock predictive model written by python 2.7.12

2. Linear regression is used in order to predict whether tomorrow's stock price will be going up or down.

3. There are tree vectors.
  (1)The fluctuation　of high price - low price today.
  (2)The fluctuation　of today stock price - yesterday stock price.
  (3)The fluctuation　of today volume - yesterday volume.
  
4. This program design is the below.
  (1)create dataset
     get_rawdata()       - get stock data from google finance and extract required data
     create_datatable()  - change data format from list to array.
     create_dataset()    - calculate three feature vectors and one label vector.
     
5. (2)build stock predictive model
     create model by using 'linear regression model' on sklearn library.
     apply_model()       - print the result (up or down).
     cal_accuracy()      - calculate and print this model’s accuracy.
     
6. apply to stock predictive model
   run entire functions and print the result(up or down, accuracy) by using 'StockPredictModel' class.

EOF 

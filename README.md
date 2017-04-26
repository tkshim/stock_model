* This code is stock predictive model written by python 2.7.12
* Linear regression is used in order to predict whether tomorrow's stock price will be going up or down.
* These three vectors are applied to this linear regression model.
  * The fluctuation of high price - low price today.
  * The fluctuation of today stock price - yesterday stock price.
  * The fluctuation of today volume - yesterday volume.
  
* This program design is the below.
  * create dataset
    * get_rawdata()       - get stock data from google finance and extract required data
    * create_datatable()  - change data format from list to array.
    * create_dataset()    - calculate three feature vectors and one label vector.
  * build model
    * create model by using 'linear regression model' on sklearn library.
    * apply_model()       - print the result (up or down).
    * cal_accuracy()      - calculate and print this model’s accuracy.
  * apply to model
    * run entire functions and print the result(up or down, accuracy) by using 'StockPredictModel' class.
* EOF

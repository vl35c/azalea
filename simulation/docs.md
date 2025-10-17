# Stock

Stock is a class that contains all of the data of the stocks

### PROPERTIES
`all_time` - stores all time highs and lows of the stock\
`bound` - stores the current ceiling and floor values for the graph to map with\
`current_day` - stores the daily highs and lows of the stock\
`historic_price` - stores the prices over time in a dictionary\
`name` - the name of the stock\
`share_value` - the current share value of the stock\
`total_shares` - the amount of shares of the stock\
`variance` - local instance of the Variance class

### METHODS
`change_value(self, value: float)` - changes the stocks current value by a percentage passed in\
\
`value` - a float passed in to change the stock price

---
`set_value(self, value: float)` - sets the current stock price to a value passed in\
\
`value` - the value to set the stock price to

---
`store_value_data(self)` - checks the current stock price against the all time and daily extremes

---
`update_price_record(self, date: int)` - stores the stock's data in the `historic_price` property and resets for the next day\
\
`date` - the integer value to be used as the key in the dictionary

---

# StockList

StockList is a list of stocks

### PROPERTIES
`stock_list` - list of stocks

### METHODS
`add_stock(self, name: str, share_value: float, total_shares: int)` - initialises a stock object and then adds it to the `stock_list`

---
`load_stocks(self, filename: str)` - loads in stocks from a pre-made csv file\
\
`file_name` - name of the file to be loaded

---
`select_names(self)` - returns a list of all stocks names

---
`select_stock(self, name: str) -> Stock | None` - allows user to input a string and returns the stock whose name matches the input\
\
`name` - string of the stock name to be found

---
`select_stocks(self, user_input: str) -> list[str]` - allows user to input a string and returns up to the first 4 stocks whose name contains that string\
\
`user_input` - the string to be searched for

---
`stock_names(self) -> list[str]` - returns a list of the name of the stocks

---

# Variance

Variance is a class which creates a pseudo-random fluctuation for simulating the stocks

### PROPERTIES
`__stock_price` - price of the stock\
`__total` - the value of which to modify the stock by : >0 increases, <0 decreases

### METHODS
`iterate(self) -> float` - calculate and return a value of which to modify the stock price by

---
```

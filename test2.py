# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import csv
import resource
import os

def trades2():

    # define column names
    col_names = ['Time', 'Symbol', 'Shares', 'Price']

    # import file. no header as first row has data. set column names
    df = pd.read_csv('/Users/davidesecoli/Downloads/input.csv', names=col_names, header=None)


    symbols = {}
    get_time = {}
    wap_price = {}
    wap_quantity = {}

    for line in df.itertuples(name=None):
        if line[2] not in symbols:
            # line[0] == will be dedicated to WAP
            # line[1] == time
            # line[2] == symbol
            # line[3] == quantity
            # line[4] == price
            symbols[line[2]] = list(line[1:])

            #swap first and second element in the list
            symbols[line[2]][0], symbols[line[2]][1] = symbols[line[2]][1], symbols[line[2]][0]

            # create new list item for WAP
            symbols[line[2]].append(0)

            # swap third and fourth elements in the list
            symbols[line[2]][3], symbols[line[2]][4] = symbols[line[2]][4], symbols[line[2]][3]

            # get_time[0] = symbol
            # get_time[1] = time

            get_time[line[2]] = line[1]

            # calculate first line of  wap for later
            wap_price[line[2]] = (line[3] * line[4])
            wap_quantity[line[2]] = line[3]

            # set time to zero
            symbols[line[2]][1] = 0

        else:

            # MAX TIME GAP
            # checks if new line symbol is equal to symbols already in the dictionary
            if line[2] == symbols[line[2]][0]:

                # set variable storing new line time minus previous time
                if symbols[line[2]][1] == 0:
                    current_time_gap = line[1] - get_time[line[2]]
                    get_time[line[2]] = line[1]

                else:
                    current_time_gap = line[1] - get_time[line[2]]
                    get_time[line[2]] = line[1]

                # check if the time for new line symbols minus previous time is greater than current max_gap
                if current_time_gap > symbols[line[2]][1]:
                    symbols[line[2]][1] = current_time_gap



                # add number of shares
                symbols[line[2]][2] += line[3]

                # calculate price times quantity per WAP
                wap_price[line[2]] += (line[3] * line[4])
                wap_quantity[line[2]] += line[3]
                symbols[line[2]][3] = int(wap_price[line[2]] / wap_quantity[line[2]])

                # update max price
                if line[4] > symbols[line[2]][4]:
                    symbols[line[2]][4] = line[4]


                # symbol[0] == symbol
                # symbol[1] == time
                # symbol[2] == quantity
                # symbol[3] == price
                # symbols[4] == vwap

    for key in sorted(symbols):
        print(symbols[key])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trades2()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/

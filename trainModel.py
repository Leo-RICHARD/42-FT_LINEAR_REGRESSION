#!/usr/bin/env python3

import pandas
import json

theta0 = 0
theta1 = 0
learningRate = 0.01

miles = []
price = []
n_miles = []
n_price = []
m = 0

try:
        with open("data.csv") as f:
            df = pandas.read_csv(f)
            if ('km' in df.columns and 'price' in df.columns):
                miles = df['km'].tolist()
                price = df['price'].tolist()
                m = len(miles)
                if (m < 2 or
                    m != len(price) or
                    not (all(isinstance(x, (int, float)) & isinstance(y, (int, float)) & (x >= 0) & (y >= 0) for x, y in zip(miles, price)))):
                    print("error:\n\tcorrupt or missing data in csv file.\nexiting")
                    exit()
            else:
                print("error:\n\tmissing 'km' and/or 'price' column in csv file\nexiting")
                exit()

except Exception as e:
    print("error retrieving data:\n\t", e, "\nexiting")
    exit()

m_min = min(miles)
m_max = max(miles)
p_min = min(price)
p_max = max(price)

def get_min(lst):
    min = lst[0]
    for x in lst:
        if x < min:
            min = x
    return min
    
def get_max(lst):
    max = lst[0]
    for x in lst:
        if x > max:
            max = x
    return max

def norm(lst, what):
    norm = []
    min = m_min if (what) else p_min
    max = m_max if (what) else p_max
    if (min == max):
        for x in lst:
            norm.append(1)
    else:
        for x in lst:
            norm.append((x - min)/(max - min))
    return norm

def estimatePrice(mileage, th1, th0):
    return (th1 * mileage + th0)
    
def cost(w, b):
    cost = 0
    for i in range(m):
        cost += (estimatePrice(n_miles[i], w, b) - n_price[i])**2    
    return (cost / (2 * m))
    
def train():
    global theta0
    global theta1
    global n_miles
    global n_price
    n_miles = norm(miles, 1)
    n_price = norm(price, 0)
    tmpTheta0 = 0
    tmpTheta1 = 0
    
    while 1:
        
        slopew = 0
        slopeb = 0
        
        for i in range(m):
            diff = (estimatePrice(n_miles[i], theta1, theta0) - n_price[i])
            slopeb += diff
            slopew += diff * n_miles[i]

        slopeb /= m
        slopew /= m
        tmpTheta1 = theta1 - (learningRate * slopew)
        tmpTheta0 = theta0 - (learningRate * slopeb)    
        if (cost(tmpTheta1, tmpTheta0) < cost(theta1, theta0)):
            theta0 = tmpTheta0
            theta1 = tmpTheta1
        else:
            return

train()

try:
    with open("values.json", 'w') as f:
        pass
        json.dump((theta0, theta1, m_min, m_max, p_min, p_max), f)
except Exception as e:
    print("error writing data:", e, "\nexiting")
    exit(1)

print("model trained")

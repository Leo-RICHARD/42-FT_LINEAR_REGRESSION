#!/usr/bin/env python3

import pandas
import json
import matplotlib.pyplot as plt

theta0 = 0
theta1 = 0

miles = []
price = []
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
                    exit(1)
            else:
                print("error:\n\tmissing 'km' and/or 'price' column in csv file\nexiting")
                exit(1)
   
        with open("values.json", 'r') as f:
            theta0, theta1, m_min, m_max, p_min, p_max = json.load(f)
            if (not isinstance(theta0, (int, float)) or
                not isinstance(theta1, (int, float)) or
                not isinstance(m_min, (int, float)) or
                not isinstance(p_min, (int, float)) or
                not isinstance(m_max, (int, float)) or
                not isinstance(p_max, (int, float))) :
                print("error:\n\tcorrupt values in json file\nexiting")
                exit(1)

except Exception as e:
    print("error retrieving data:\n\t", e, "\nexiting")
    exit(1)

rm_min = min(miles)
rm_max = max(miles)
rp_min = min(price)
rp_max = max(price)

def n_estimatePrice(mileage, th1, th0):
	return (th1 * mileage + th0)
	
def estimatePrice(mileage, th1, th0):
    if (m_max != m_min):
        mileage = (mileage - m_min) / (m_max - m_min)
    else:
        mileage = 1
    pred = n_estimatePrice(mileage, th1, th0)
    if (p_max != p_min):
	    pred = pred * (p_max - p_min) + p_min
    else:
        pred = p_min
    return (pred)

plt.title("linear regression model")
plt.xlabel("mileage")
plt.ylabel("price")
plt.xlim(rm_min - 0.25 * (rm_max - rm_min), rm_max + 0.25 * (rm_max - rm_min))
plt.ylim(rp_min - 0.25 * (rp_max - rp_min), rp_max + 0.25 * (rp_max - rp_min))
plt.scatter(miles, price, label="dataset")
plt.plot([plt.xlim()[0], plt.xlim()[1]], [estimatePrice(plt.xlim()[0], theta1, theta0), estimatePrice(plt.xlim()[1], theta1, theta0)], label="predictions", color=(245/255, 194/255, 17/255))
plt.legend()
plt.show()



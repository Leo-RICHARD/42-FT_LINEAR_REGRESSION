#!/usr/bin/env python3

import json

theta0 = 0
theta1 = 0
mileage = 0
m_min = 0
m_max = 0
p_max = 0
p_min = 0

try:
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
    if (pred < 0):
        pred = 0
    return (pred)

while (1):
    mileage = input("Enter mileage : ")
    try:
        mileage = float(mileage)
        if (mileage >= 0):
            print("Estimated price :", estimatePrice(mileage, theta1, theta0))
            exit(0)
        else:
            throw(Exception)
    except Exception:
        print("No")

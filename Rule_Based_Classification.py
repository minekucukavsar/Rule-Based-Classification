#Rule Based Classification

import pandas as pd
import numpy as np

df=pd.read_csv("C:/Users/hp/PycharmProjects/pythonProject2/persona.csv")


def check_df(df, head = 5):
    print("============ head ============")
    print(df.head(head))

    print("============ tail ============")
    print(df.tail(head))

    print("============ types ============")
    print(df.dtypes)

    print("============ shape ============")
    print(df.shape)

    print("============ NA ============")
    print(df.isnull().sum())

    print("============ quantiles ============")
    print(df.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# Let's see how many unique resources there are.
df.columns
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Let's see how many unique prices there are
df["PRICE"].nunique()
df["PRICE"].value_counts()

#We can see how many sales came from countries.
df["COUNTRY"].value_counts()

# How much was earned in total from sales by country?
df[["COUNTRY","PRICE"]].groupby("COUNTRY").agg({"sum"})

# Related to "SOURCE" types, what are the sales numbers?
df["SOURCE"].value_counts()

# According to do countries, what are the mean of "PRICE"?
df[["COUNTRY","PRICE"]].groupby("COUNTRY").agg({"PRICE" : "mean"})


# What are the PRICE averages by SOURCES?
df[["SOURCE", "PRICE"]].groupby("SOURCE").agg({"PRICE" : "mean"})


# What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df[["COUNTRY", "PRICE", "SOURCE"]].groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean"})


# What are the average earnings in country, source, sex, age breakdown?

deg_group = ["COUNTRY", "SOURCE", "SEX", "AGE"]

agg_df = df.groupby(deg_group).agg({"PRICE": "mean"})
agg_df.sort_values("PRICE",ascending=False)


# Converting index names to variable names
agg_df=agg_df.reset_index()

agg_df[["AGE"]]


# Converting age variable to categorical variable and adding it into agg_df.
agg_df["AGE_CAT"]=pd.cut(agg_df["AGE"],[0,18,23,30,40,70],labels = ["0_18","19_23","24_30","31_40","41_70"])
agg_df[["AGE_CAT"]]


# Let's define new level-based customers
agg_df["customers_level_based"] = [(row[0] + "_" + row[1] + "_" + row[2]).upper() + "_" + row[5] for row in agg_df.values]
agg_df = agg_df[["customers_level_based", "PRICE"]].groupby("customers_level_based").agg({"PRICE" : "mean"})
agg_df = agg_df.reset_index()



# Let's divide new customers into 4 segments

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels= ["D","C","B","A"])

agg_df

agg_df[["SEGMENT","PRICE"]].groupby("SEGMENT").agg(["mean", "max", "sum"])

agg_df[agg_df["SEGMENT"]=="C"].describe().T

#Which segment belongs to a 33-year-old Turkish woman using android, and how much income is expected to earn on average.
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# Which segment does a 35-year-old french woman using iOS belong to, and how much income is expected to earn on average.
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]



import pandas as pd

# df means dataframe

# Data 1. Global total
global_df = pd.read_csv("data/09-12-2020.csv")
global_totals = (
    global_df[["Confirmed", "Deaths", "Recovered"]]
    .sum()
    .reset_index(name="count")
    .rename(columns={"index": "condition"})
)

# Data 2. Country total
country_df = global_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
country_totals = (
    country_df.groupby("Country_Region")
    .sum()
    .sort_values(by="Confirmed", ascending=False)
    .reset_index()
)

# Data 3. Per Condition (Global and Country)
conditions = ["confirmed", "deaths", "recovered"]


def make_country_df(country):
    def make_df(condition):
        df = pd.read_csv(f"data/time_{condition}.csv")
        df = df.loc[df["Country/Region"] == country]
        df = (
            df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


def make_global_df():
    def make_df(condition):
        df = pd.read_csv(f"data/time_{condition}.csv")
        df = (
            df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


# Dash Core Component - Dropdown
dropdown_options = country_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]
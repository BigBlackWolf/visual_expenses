import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime


def import_data(path) -> pd.DataFrame:
    df = pd.read_csv(path, delimiter=";")
    df.columns.values[0] = "unblock_day"
    df.columns.values[1] = "pay_day"
    df.columns.values[2] = "description"
    df.columns.values[3] = "sender_receiver"
    df.columns.values[4] = "account_number"
    df.columns.values[5] = "amount"
    df.columns.values[6] = "account_state"
    df.columns.values[7] = "id"
    df.columns.values[8] = "unnamed"

    # df.drop("description", axis=1, inplace=True)
    df.drop("sender_receiver", axis=1, inplace=True)
    df.drop("account_number", axis=1, inplace=True)
    df.drop("unnamed", axis=1, inplace=True)
    df.drop("id", axis=1, inplace=True)
    df.drop("account_state", axis=1, inplace=True)
    df.drop("unblock_day", axis=1, inplace=True)

    df["pay_day"] = pd.to_datetime(df["pay_day"], format="%d-%m-%Y")
    df["pay_day"] = df["pay_day"].apply(lambda x: x.strftime("%Y-%m"))
    df["pay_day"] = pd.to_datetime(df["pay_day"], format="%Y-%m")


    df["amount"] = df["amount"].apply(lambda x: round(float(x.replace(",", ".")), 0))
    df.loc[df["amount"] < -60000, "amount"] = -1

    df["expense"] = df["amount"].apply(lambda x: False if x > 0 else True)
    # df["unblock_day"] = pd.to_datetime(df["unblock_day"], format="%d-%m-%Y")
    # df = df.sort_values(by=["initial_date"], ascending=False)

    return df


def group_by_month(df: pd.DataFrame):
    new_df = df.groupby(["pay_day", "expense"])["amount"].sum().reset_index()
    new_df = new_df.sort_values(by="pay_day")
    diff = new_df.groupby("pay_day")["amount"].sum()
    separate_column = pd.DataFrame({"pay_day": diff.index, "saldo": diff.values})
    new_df = pd.merge(new_df, separate_column)
    return new_df


def visualize_data(df: pd.DataFrame):
    expenses_df = df[df["amount"] < 0]
    income_df = df[df["amount"] > 0]

    bar1 = go.Bar(
        x=expenses_df["pay_day"],
        y=income_df["amount"],
        name="Income",
    )
    bar2 = go.Bar(
        x=expenses_df["pay_day"],
        y=expenses_df["amount"],
        name="Expenses",
    )

    line1 = go.Scatter(
        x=expenses_df["pay_day"],
        y=expenses_df["saldo"],
        name="Saldo",
        mode="lines+markers",
        text=expenses_df["saldo"],
        textfont=dict(
            size=18,
            color="yellow"
        )
    )

    figure = go.Figure(
        [bar1, bar2, line1]
    )
    figure.update_layout(barmode='relative')
    figure.show()


def main():
    path = "/Users/bigblackwolf/vscode_projects/cashflow_analysis/historia/PLN.csv"
    df = import_data(path)
    new_df = group_by_month(df)

    # a = new_df[new_df["pay_day"] > datetime.datetime(month=4, year=2023, day=1)]
    # print(a)
    
    visualize_data(new_df)

    # total = new_df["amount"].sum()
    # print(round(total, 2))


if __name__ == "__main__":
    main()

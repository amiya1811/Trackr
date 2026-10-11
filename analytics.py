import pandas as pd

FIXED_CATEGORIES = {"Rent", "Bills & Utilities", "Health"}

def summarize(df):
    if df.empty: return 0.0, 0.0, 0.0, 0
    exp = float(df.loc[df["type"]=="Expense","amount"].sum())
    inc = float(df.loc[df["type"]=="Income","amount"].sum())
    return exp, inc, inc-exp, len(df)

def category_totals(df):
    if df.empty: return pd.DataFrame(columns=["category","amount"])
    exp = df[df["type"]=="Expense"]
    if exp.empty: return pd.DataFrame(columns=["category","amount"])
    return exp.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)

def monthly_totals(df, include_income=False):
    if df.empty: return pd.DataFrame(columns=["month","Expense","Income"])
    work = df.copy()
    work["month"] = pd.to_datetime(work["date"], errors="coerce").dt.to_period("M").astype(str)
    work = work.dropna(subset=["month"])
    pivot = work.pivot_table(index="month", columns="type", values="amount", aggfunc="sum", fill_value=0).reset_index()
    for col in ["Expense","Income"]:
        if col not in pivot: pivot[col] = 0.0
    pivot = pivot.sort_values("month")
    return pivot if include_income else pivot[["month","Expense"]].rename(columns={"Expense":"amount"})

def spending_insights(df):
    if df.empty: return []
    exp = df[df["type"]=="Expense"].copy()
    if exp.empty: return ["No expenses recorded yet. Add transactions to start seeing spending insights."]
    out = []
    total = float(exp["amount"].sum())
    cats = exp.groupby("category")["amount"].sum().sort_values(ascending=False)
    if len(cats):
        top_cat = cats.index[0]
        share = cats.iloc[0] / total * 100 if total else 0
        out.append(f"{top_cat} is your largest recorded expense category at {share:.0f}% of total expenses.")
    exp["month"] = pd.to_datetime(exp["date"], errors="coerce").dt.strftime("%Y-%m")
    monthly = exp.groupby("month")["amount"].sum().sort_index()
    if len(monthly) >= 2:
        old, new = float(monthly.iloc[-2]), float(monthly.iloc[-1])
        if old:
            change = (new-old)/old*100
            if change >= 15: out.append(f"Expenses increased by {change:.0f}% compared with the previous recorded month.")
            elif change <= -15: out.append(f"Expenses decreased by {abs(change):.0f}% compared with the previous recorded month.")
            else: out.append("Your latest recorded month's expenses are broadly in line with the previous month.")
    if len(exp) >= 5:
        avg = exp.groupby("category")["amount"].mean().sort_values(ascending=False)
        if len(avg): out.append(f"Your average transaction is ₹{exp['amount'].mean():,.0f}; largest average ticket category: {avg.index[0]}.")
    return out[:4]

def detect_patterns(df):
    if df.empty: return []
    exp = df[df["type"]=="Expense"].copy()
    if len(exp) < 5: return ["Add at least five expense entries for a more useful pattern scan."]
    out = []
    q1 = exp["amount"].quantile(.25); q3 = exp["amount"].quantile(.75); iqr = q3-q1
    threshold = q3 + 1.5*iqr
    high = exp[exp["amount"] > threshold]
    if not high.empty:
        row = high.sort_values("amount", ascending=False).iloc[0]
        out.append(f"Unusually large entry to review: “{row['description']}” at ₹{row['amount']:,.0f}. This is a statistical outlier, not a fraud finding.")
    exp["month"] = pd.to_datetime(exp["date"], errors="coerce").dt.strftime("%Y-%m")
    monthcat = exp.groupby(["month","category"])["amount"].sum().reset_index()
    if len(monthcat["month"].unique()) >= 2:
        cat_month = monthcat.pivot(index="month", columns="category", values="amount").fillna(0).sort_index()
        if len(cat_month) >= 2:
            changes = cat_month.iloc[-1] - cat_month.iloc[-2]
            if len(changes) and changes.max() > 0:
                c = changes.idxmax()
                if changes[c] > 0: out.append(f"{c} spending rose by ₹{changes[c]:,.0f} compared with the previous recorded month.")
    repeated = exp.groupby("description")["id"].count()
    repeats = repeated[repeated >= 3]
    if len(repeats): out.append(f"Repeated description detected: “{repeats.index[0]}” appears {int(repeats.iloc[0])} times; check if it is a recurring expense.")
    return out[:4]

def fixed_variable_totals(df):
    if df.empty: return 0.0, 0.0
    exp = df[df["type"]=="Expense"]
    fixed = float(exp[exp["category"].isin(FIXED_CATEGORIES)]["amount"].sum())
    variable = float(exp[~exp["category"].isin(FIXED_CATEGORIES)]["amount"].sum())
    return fixed, variable

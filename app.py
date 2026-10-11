import os
from datetime import date, datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from database import init_db, get_connection, add_transaction, update_transaction, delete_transaction, get_transactions, set_budget, get_budgets, add_goal, get_goals, update_goal, seed_demo_data, clear_demo_data
from analytics import summarize, category_totals, monthly_totals, spending_insights, detect_patterns, fixed_variable_totals
from charts import donut_chart, bar_chart, line_chart
from styles import apply_styles

st.set_page_config(page_title="Expense Tracker with Data Visualization using Pandas and Matplotlib | Trackr", page_icon="💸", layout="wide", initial_sidebar_state="expanded")
init_db()
apply_styles()

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def money(value):
    return f"₹{float(value or 0):,.0f}"

def get_df():
    return get_transactions()

def page_header(title, subtitle):
    st.markdown(f'<div class="page-heading"><div><h1>{title}</h1><p>{subtitle}</p></div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-mark">T</div><div><div class="brand-name">Trackr</div><div class="brand-tag">Pandas + Matplotlib</div></div></div>', unsafe_allow_html=True)
    st.markdown("---")
    pages = ["Dashboard", "Transactions", "Budget & Expenses", "Spending Analytics", "Reports", "Goals & Savings", "Settings"]
    icons = {"Dashboard":"◫", "Transactions":"↔", "Budget & Expenses":"▤", "Spending Analytics":"◷", "Reports":"▧", "Goals & Savings":"◎", "Settings":"⚙"}
    for p in pages:
        if st.button(f"{icons[p]}   {p}", key=f"nav_{p}", use_container_width=True, type="primary" if st.session_state.page == p else "secondary"):
            st.session_state.page = p
            st.rerun()
    st.markdown('<div class="sidebar-bottom"><span class="status-dot"></span> Local database connected</div>', unsafe_allow_html=True)
    st.caption("Your financial data stays on this device.")

df = get_df()
page = st.session_state.page

# shared filters
with st.container():
    top1, top2, top3 = st.columns([3, 1.2, 1.2])
    with top1:
        st.markdown('<div class="eyebrow">EXPENSE TRACKER · PANDAS DATA ANALYSIS · MATPLOTLIB VISUALIZATION</div>', unsafe_allow_html=True)
    with top2:
        selected_month = st.selectbox("Month", ["All time"] + sorted(df["month"].dropna().unique().tolist(), reverse=True) if not df.empty else ["All time"], label_visibility="collapsed", key="global_month")
    with top3:
        if st.button("＋  Add expense", type="primary", use_container_width=True):
            st.session_state.page = "Transactions"
            st.session_state.show_add = True
            st.rerun()

filtered = df.copy()
if selected_month != "All time" and not filtered.empty:
    filtered = filtered[filtered["month"] == selected_month]

if page == "Dashboard":
    page_header("Your money, in focus.", "A clearer view of your spending, budgets, and progress.")
    total, income, balance, count = summarize(filtered)
    prev_month = (date.today().replace(day=1) - pd.Timedelta(days=1)).strftime("%Y-%m")
    prev = df[df["month"] == prev_month] if not df.empty else df
    prev_total = float(prev.loc[prev["type"] == "Expense", "amount"].sum()) if not prev.empty else 0
    change = ((total-prev_total)/prev_total*100) if prev_total else 0
    k1,k2,k3,k4 = st.columns(4)
    with k1: st.markdown(f'<div class="metric-card"><div class="metric-label">TOTAL EXPENSES</div><div class="metric-value">{money(total)}</div><div class="metric-foot">Selected period</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="metric-card"><div class="metric-label">TOTAL INCOME</div><div class="metric-value">{money(income)}</div><div class="metric-foot">Recorded income</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="metric-card"><div class="metric-label">NET CASH FLOW</div><div class="metric-value">{money(income-total)}</div><div class="metric-foot">Income minus expenses</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="metric-card"><div class="metric-label">TRANSACTIONS</div><div class="metric-value">{count}</div><div class="metric-foot">Entries in selected period</div></div>', unsafe_allow_html=True)
    st.write("")
    left,right = st.columns([1.4,1])
    with left:
        st.markdown('<div class="section-title">Monthly spending trend <span>Expense overview</span></div>', unsafe_allow_html=True)
        mt = monthly_totals(df)
        if mt.empty: st.info("Add transactions to see your spending trend.")
        else: st.pyplot(line_chart(mt), use_container_width=True)
    with right:
        st.markdown('<div class="section-title">Where it goes <span>Category breakdown</span></div>', unsafe_allow_html=True)
        ct = category_totals(filtered)
        if ct.empty: st.info("Your category breakdown will appear here.")
        else: st.pyplot(donut_chart(ct), use_container_width=True)
    left,right = st.columns([1,1])
    with left:
        st.markdown('<div class="section-title">Budget snapshot <span>Monthly limits</span></div>', unsafe_allow_html=True)
        budgets = get_budgets()
        month_now = date.today().strftime("%Y-%m")
        current = df[(df["month"] == month_now) & (df["type"] == "Expense")] if not df.empty else df
        if budgets.empty:
            st.info("Set a monthly budget in Budget & Expenses to track your limits.")
        else:
            for _, b in budgets.iterrows():
                spent = float(current[current["category"] == b["category"]]["amount"].sum())
                pct = min(spent / float(b["amount"]), 1.0) if float(b["amount"]) else 0
                st.markdown(f"**{b['category']}** <span class='muted'>{money(spent)} of {money(b['amount'])}</span>", unsafe_allow_html=True)
                st.progress(pct, text=f"{pct*100:.0f}% used")
    with right:
        st.markdown('<div class="section-title">Spending insights <span>Rule-based observations</span></div>', unsafe_allow_html=True)
        insights = spending_insights(df)
        if not insights: st.success("You're all set. Add more transactions to unlock useful observations.")
        for insight in insights[:4]:
            st.markdown(f'<div class="insight">{insight}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent transactions <span>Latest activity</span></div>', unsafe_allow_html=True)
    if filtered.empty: st.info("No transactions yet. Add an expense or load demo data in Settings.")
    else:
        show = filtered.sort_values(["date","id"], ascending=False).head(6)
        st.dataframe(show[["date","description","category","type","payment_method","amount"]].rename(columns={"date":"Date","description":"Description","category":"Category","type":"Type","payment_method":"Payment method","amount":"Amount (₹)"}), use_container_width=True, hide_index=True)

elif page == "Transactions":
    page_header("Transactions", "Every inflow and outflow, organized in one place.")
    with st.expander("＋ Add a transaction", expanded=st.session_state.pop("show_add", False)):
        with st.form("add_transaction_form", clear_on_submit=True):
            a,b,c = st.columns(3)
            tdate = a.date_input("Date", value=date.today())
            desc = b.text_input("Description", placeholder="e.g. Groceries")
            typ = c.selectbox("Type", ["Expense","Income"])
            d,e,f = st.columns(3)
            amount = d.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
            category = e.selectbox("Category", ["Food & Dining","Transport","Shopping","Bills & Utilities","Health","Entertainment","Education","Travel","Rent","Salary","Freelance","Other"])
            method = f.selectbox("Payment method", ["UPI","Cash","Card","Bank transfer","Wallet","Other"])
            note = st.text_input("Notes (optional)")
            submitted = st.form_submit_button("Save transaction", type="primary")
            if submitted:
                if not desc.strip() or amount <= 0: st.error("Enter a description and an amount greater than zero.")
                else:
                    add_transaction(tdate.isoformat(), desc.strip(), category, typ, float(amount), method, note.strip(), 0)
                    st.success("Transaction saved.")
                    st.rerun()
    c1,c2,c3 = st.columns([2,1,1])
    with c1: query = st.text_input("Search transactions", placeholder="Search description, category, notes…")
    with c2: type_filter = st.selectbox("Type", ["All","Expense","Income"])
    with c3: cat_filter = st.selectbox("Category", ["All"] + sorted(df["category"].dropna().unique().tolist()) if not df.empty else ["All"])
    view = df.copy()
    if query and not view.empty:
        view = view[view.apply(lambda r: query.lower() in " ".join(map(str,r.values)).lower(), axis=1)]
    if type_filter != "All": view = view[view["type"] == type_filter]
    if cat_filter != "All": view = view[view["category"] == cat_filter]
    st.markdown(f"**{len(view)} transactions**")
    if not view.empty:
        st.dataframe(view[["id","date","description","category","type","payment_method","amount","notes"]].rename(columns={"id":"ID","date":"Date","description":"Description","category":"Category","type":"Type","payment_method":"Payment","amount":"Amount (₹)","notes":"Notes"}), use_container_width=True, hide_index=True)
        with st.expander("Edit or delete a transaction"):
            ids = view["id"].astype(int).tolist()
            chosen = st.selectbox("Select transaction ID", ids)
            row = view[view["id"] == chosen].iloc[0]
            with st.form("edit_tx_form"):
                x1,x2,x3 = st.columns(3)
                edate = x1.date_input("Date", value=pd.to_datetime(row["date"]).date(), key="edate")
                edesc = x2.text_input("Description", value=row["description"], key="edesc")
                etype = x3.selectbox("Type", ["Expense","Income"], index=["Expense","Income"].index(row["type"]), key="etype")
                y1,y2,y3 = st.columns(3)
                eamount = y1.number_input("Amount (₹)", min_value=0.01, value=float(row["amount"]), step=100.0, key="eamount")
                cats = ["Food & Dining","Transport","Shopping","Bills & Utilities","Health","Entertainment","Education","Travel","Rent","Salary","Freelance","Other"]
                ecat = y2.selectbox("Category", cats, index=cats.index(row["category"]) if row["category"] in cats else len(cats)-1, key="ecat")
                emethod = y3.selectbox("Payment", ["UPI","Cash","Card","Bank transfer","Wallet","Other"], key="emethod", index=["UPI","Cash","Card","Bank transfer","Wallet","Other"].index(row["payment_method"]) if row["payment_method"] in ["UPI","Cash","Card","Bank transfer","Wallet","Other"] else 0)
                enotes = st.text_input("Notes", value=str(row["notes"] or ""), key="enotes")
                s1,s2 = st.columns(2)
                save = s1.form_submit_button("Save changes", type="primary")
                delete = s2.form_submit_button("Delete transaction")
                if save:
                    update_transaction(int(chosen), edate.isoformat(), edesc.strip(), ecat, etype, float(eamount), emethod, enotes)
                    st.success("Transaction updated."); st.rerun()
                if delete:
                    delete_transaction(int(chosen)); st.warning("Transaction deleted."); st.rerun()
    else: st.info("No transactions match these filters.")
    st.markdown("### Import / export CSV")
    ex1,ex2 = st.columns(2)
    with ex1:
        export_df = df.drop(columns=["month"], errors="ignore")
        st.download_button("Download all transactions", export_df.to_csv(index=False).encode("utf-8"), "trackr_transactions.csv", "text/csv", use_container_width=True)
    with ex2:
        upload = st.file_uploader("Import CSV", type=["csv"], help="Required columns: date, description, category, type, amount. Optional: payment_method, notes.")
        if upload:
            try:
                imp = pd.read_csv(upload)
                required = {"date","description","category","type","amount"}
                if not required.issubset(set(imp.columns)):
                    st.error("CSV is missing required columns: " + ", ".join(sorted(required-set(imp.columns))))
                else:
                    st.dataframe(imp.head(8), use_container_width=True, hide_index=True)
                    if st.button(f"Import {len(imp)} rows", type="primary"):
                        ok, bad = 0, 0
                        for _, r in imp.iterrows():
                            try:
                                d = pd.to_datetime(r["date"], errors="raise").date().isoformat()
                                desc = str(r["description"]).strip()
                                cat = str(r["category"]).strip()
                                typ = str(r["type"]).strip().title()
                                amt = float(r["amount"])
                                if not desc or typ not in ["Expense","Income"] or amt <= 0: raise ValueError()
                                add_transaction(d, desc, cat or "Other", typ, amt, str(r.get("payment_method","Other")), str(r.get("notes","")), 0)
                                ok += 1
                            except Exception: bad += 1
                        st.success(f"Imported {ok} rows. Skipped {bad} invalid rows.")
                        st.rerun()
            except Exception as exc: st.error(f"Could not read CSV: {exc}")

elif page == "Budget & Expenses":
    page_header("Budget & expenses", "Set sensible limits and keep your spending intentional.")
    st.markdown('<div class="section-title">Set category budget <span>Monthly recurring limit</span></div>', unsafe_allow_html=True)
    with st.form("budget_form"):
        b1,b2 = st.columns(2)
        bcat = b1.selectbox("Category", ["Food & Dining","Transport","Shopping","Bills & Utilities","Health","Entertainment","Education","Travel","Rent","Other"])
        bamt = b2.number_input("Monthly budget (₹)", min_value=1.0, value=5000.0, step=500.0)
        if st.form_submit_button("Save budget", type="primary"):
            set_budget(bcat, float(bamt)); st.success("Budget saved."); st.rerun()
    budgets = get_budgets()
    this_month = date.today().strftime("%Y-%m")
    month_df = df[(df["month"] == this_month) & (df["type"] == "Expense")] if not df.empty else df
    if budgets.empty: st.info("No category budgets yet.")
    else:
        for _, b in budgets.iterrows():
            spent = float(month_df[month_df["category"] == b["category"]]["amount"].sum())
            limit = float(b["amount"]); pct = spent / limit if limit else 0
            st.markdown(f"**{b['category']}** — {money(spent)} / {money(limit)}")
            st.progress(min(pct,1.0), text=("Over budget" if pct > 1 else f"{pct*100:.0f}% used"))
    st.markdown('<div class="section-title">Expense type split <span>Fixed vs. variable</span></div>', unsafe_allow_html=True)
    fixed, variable = fixed_variable_totals(df)
    f1,f2 = st.columns(2)
    with f1: st.markdown(f'<div class="metric-card"><div class="metric-label">FIXED / RECURRING</div><div class="metric-value">{money(fixed)}</div><div class="metric-foot">Categories like rent and bills</div></div>', unsafe_allow_html=True)
    with f2: st.markdown(f'<div class="metric-card"><div class="metric-label">VARIABLE</div><div class="metric-value">{money(variable)}</div><div class="metric-foot">Day-to-day flexible spending</div></div>', unsafe_allow_html=True)
    st.caption("This split uses category rules; you can change categories from Transactions.")

elif page == "Spending Analytics":
    page_header("Spending analytics", "Explore your habits with clear, practical visuals.")
    if df.empty: st.info("Add transactions or load demo data in Settings to view analytics.")
    else:
        expenses = df[df["type"] == "Expense"]
        inc = df[df["type"] == "Income"]
        total_exp = float(expenses["amount"].sum()); total_inc = float(inc["amount"].sum())
        a,b,c = st.columns(3)
        a.metric("All-time expenses", money(total_exp))
        b.metric("All-time income", money(total_inc))
        c.metric("Savings rate", f"{max(0,(total_inc-total_exp)/total_inc*100):.1f}%" if total_inc else "—")
        l,r = st.columns(2)
        with l:
            st.markdown('<div class="section-title">Category spending</div>', unsafe_allow_html=True)
            ct = category_totals(expenses)
            if not ct.empty: st.pyplot(donut_chart(ct), use_container_width=True)
        with r:
            st.markdown('<div class="section-title">Income vs expenses by month</div>', unsafe_allow_html=True)
            mt = monthly_totals(df, include_income=True)
            if not mt.empty: st.pyplot(bar_chart(mt), use_container_width=True)
        st.markdown('<div class="section-title">Pattern detector</div>', unsafe_allow_html=True)
        patterns = detect_patterns(df)
        if patterns:
            for p in patterns: st.markdown(f'<div class="insight">{p}</div>', unsafe_allow_html=True)
        else: st.info("More transaction history will help identify spending patterns.")
        st.markdown('<div class="section-title">Category totals</div>', unsafe_allow_html=True)
        st.dataframe(ct.rename(columns={"category":"Category","amount":"Total (₹)"}), use_container_width=True, hide_index=True)

elif page == "Reports":
    page_header("Reports", "Export a clean snapshot of your financial activity.")
    if df.empty: st.info("There are no transactions to report yet.")
    else:
        months = ["All time"] + sorted(df["month"].dropna().unique().tolist(), reverse=True)
        report_month = st.selectbox("Report period", months, key="report_month")
        rep = df if report_month == "All time" else df[df["month"] == report_month]
        exp = float(rep.loc[rep["type"]=="Expense","amount"].sum())
        inc = float(rep.loc[rep["type"]=="Income","amount"].sum())
        a,b,c = st.columns(3); a.metric("Expenses",money(exp)); b.metric("Income",money(inc)); c.metric("Net",money(inc-exp))
        st.markdown("### Category summary")
        ct = category_totals(rep)
        if not ct.empty: st.dataframe(ct.rename(columns={"category":"Category","amount":"Expense total (₹)"}), use_container_width=True, hide_index=True)
        report = rep.drop(columns=["month"], errors="ignore").copy()
        st.download_button("Download report CSV", report.to_csv(index=False).encode("utf-8"), f"trackr_report_{report_month.replace(' ','_')}.csv", "text/csv", type="primary")
        st.caption("CSV reports open in Excel, Google Sheets, and other spreadsheet apps.")

elif page == "Goals & Savings":
    page_header("Goals & savings", "Turn a target into steady progress.")
    with st.form("goal_form"):
        g1,g2 = st.columns(2)
        gname = g1.text_input("Goal name", placeholder="e.g. New laptop")
        target = g2.number_input("Target amount (₹)", min_value=1.0, value=50000.0, step=1000.0)
        if st.form_submit_button("Create goal", type="primary"):
            if gname.strip(): add_goal(gname.strip(), float(target)); st.success("Goal created."); st.rerun()
            else: st.error("Enter a goal name.")
    goals = get_goals()
    if goals.empty: st.info("No savings goals yet. Create your first goal above.")
    else:
        for _, g in goals.iterrows():
            with st.container(border=True):
                st.markdown(f"### {g['name']}")
                current = float(g["saved"]); target = float(g["target"]); pct = min(current/target,1) if target else 0
                st.progress(pct, text=f"{money(current)} saved of {money(target)} · {pct*100:.0f}%")
                with st.form(f"contribute_{g['id']}"):
                    amount = st.number_input("Add contribution (₹)", min_value=0.0, step=500.0, key=f"goal_amt_{g['id']}")
                    if st.form_submit_button("Add contribution"):
                        if amount > 0: update_goal(int(g["id"]), current+float(amount)); st.success("Contribution added."); st.rerun()

elif page == "Settings":
    page_header("Settings", "Manage your local workspace and demo data.")
    st.markdown('<div class="section-title">Appearance</div>', unsafe_allow_html=True)
    mode = st.radio("Theme preference", ["Dark","Light"], horizontal=True, index=0 if st.session_state.theme=="Dark" else 1)
    if mode != st.session_state.theme:
        st.session_state.theme = mode
        st.success("Theme preference saved for this session. Refresh the app to apply the alternate palette.")
    st.markdown('<div class="section-title">Demo data</div>', unsafe_allow_html=True)
    st.write("Load example transactions to explore the dashboard, charts, budgets, and reports. Existing entries are preserved.")
    if st.button("Load demo data", type="primary"):
        seed_demo_data(); st.success("Demo data loaded."); st.rerun()
    st.write("Remove only rows marked as demo data.")
    if st.button("Clear demo data"):
        clear_demo_data(); st.success("Demo data cleared."); st.rerun()
    st.markdown('<div class="section-title">Data & privacy</div>', unsafe_allow_html=True)
    st.write("Trackr stores transactions, budgets, and goals in a local SQLite database at `data/trackr.db`. No account, cloud sync, or API key is required.")
    st.warning("Back up the `data/trackr.db` file before moving or deleting your project folder.")
    st.markdown('<div class="section-title">About Trackr</div>', unsafe_allow_html=True)
    st.write("Track Smarter. Spend Better. Expense Tracker with Data Visualization using Pandas and Matplotlib. Trackr uses Pandas DataFrames for transaction cleaning, grouping, summaries, month-wise analysis, category analysis, and pattern insights; Matplotlib generates the dashboard charts.")

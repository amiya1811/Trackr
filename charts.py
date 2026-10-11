import matplotlib.pyplot as plt

def _base():
    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=120)
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    ax.tick_params(colors="#9CA3AF", labelsize=8)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.grid(axis="y", alpha=.15, linestyle="--")
    ax.set_axisbelow(True)
    return fig, ax

def donut_chart(df):
    fig, ax = plt.subplots(figsize=(5,3.2), dpi=120)
    fig.patch.set_alpha(0)
    if df.empty:
        ax.text(.5,.5,"No data yet",ha="center",va="center",color="#9CA3AF")
        ax.axis("off")
        return fig
    colors = ["#8B7CFF","#59C3C3","#F2B880","#F08080","#7AA6F9","#B7D6A6","#D8A7E8","#9CA3AF"]
    wedges, _ = ax.pie(df["amount"], startangle=90, counterclock=False, colors=colors[:len(df)], wedgeprops={"width":.32,"edgecolor":"none"})
    total = df["amount"].sum()
    ax.text(0,.08,f"₹{total:,.0f}",ha="center",va="center",fontsize=14,fontweight="bold",color="#E8EAF2")
    ax.text(0,-.17,"Total spend",ha="center",va="center",fontsize=8,color="#9CA3AF")
    labels = [f"{r.category} · ₹{r.amount:,.0f}" for r in df.head(6).itertuples()]
    ax.legend(wedges[:len(labels)], labels, loc="center left", bbox_to_anchor=(.88,.5), frameon=False, fontsize=7, labelcolor="#AEB5C5")
    ax.axis("equal")
    fig.tight_layout()
    return fig

def line_chart(df):
    fig, ax = _base()
    if df.empty:
        ax.text(.5,.5,"No data yet",ha="center",va="center",color="#9CA3AF",transform=ax.transAxes)
    else:
        x = df["month"].astype(str)
        y = df["amount"] if "amount" in df else df["Expense"]
        ax.plot(x,y, color="#8B7CFF", linewidth=2.5, marker="o", markersize=4)
        ax.fill_between(range(len(y)), y, alpha=.12, color="#8B7CFF")
        ax.set_xticks(range(len(x))); ax.set_xticklabels(x, rotation=30, ha="right")
        ax.set_ylabel("Amount (₹)", color="#9CA3AF", fontsize=8)
    fig.tight_layout()
    return fig

def bar_chart(df):
    fig, ax = _base()
    if df.empty:
        ax.text(.5,.5,"No data yet",ha="center",va="center",color="#9CA3AF",transform=ax.transAxes)
    else:
        x = range(len(df))
        if "Expense" in df:
            ax.bar([i-.18 for i in x], df["Expense"], width=.35, color="#8B7CFF", label="Expense")
            ax.bar([i+.18 for i in x], df["Income"], width=.35, color="#59C3C3", label="Income")
            ax.legend(frameon=False, labelcolor="#AEB5C5", fontsize=8)
        else: ax.bar(x, df["amount"], color="#8B7CFF", width=.55)
        ax.set_xticks(list(x)); ax.set_xticklabels(df["month"].astype(str), rotation=30, ha="right")
        ax.set_ylabel("Amount (₹)", color="#9CA3AF", fontsize=8)
    fig.tight_layout()
    return fig

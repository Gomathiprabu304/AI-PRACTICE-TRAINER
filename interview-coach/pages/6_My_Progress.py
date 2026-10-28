import streamlit as st
import pandas as pd
import altair as alt
from progress_tracker import load_progress

st.title("My Progress")
st.write("See how your practice is going across all skills.")

data = load_progress()

if len(data) == 0:
    st.info("No practice attempts yet. Try a skill from the menu on the left, then come back here.")
    st.stop()

SCORE_SKILLS = ["Listening", "Reading", "Aptitude"]
LSRW = ["Listening", "Speaking", "Reading", "Writing"]

# One row per attempt
rows = []
for entry in data:
    d = entry["details"]
    module = entry["module"]
    row = {"Time": entry["timestamp"], "Module": module}
    if module in SCORE_SKILLS:
        total = d.get("total", 0)
        score = d.get("score", 0)
        row["Result"] = f"{score} / {total}"
        row["Score %"] = round(score / total * 100) if total else 0
        row["Grammar issues"] = None
    else:
        row["Result"] = f"{d.get('grammar_issues', 0)} grammar issue(s)"
        row["Score %"] = None
        row["Grammar issues"] = d.get("grammar_issues", 0)
    rows.append(row)

df = pd.DataFrame(rows)

# Skills to show: the four LSRW skills, plus Aptitude once it has attempts
skills = list(LSRW)
if (df["Module"] == "Aptitude").sum() > 0:
    skills.append("Aptitude")

# Summary numbers
st.subheader("Summary")
cols = st.columns(len(skills) + 1)
cols[0].metric("Total attempts", len(df))
for col, name in zip(cols[1:], skills):
    col.metric(name, int((df["Module"] == name).sum()))

# Practice by skill, kept in LSRW order
st.subheader("Practice by skill")
counts = df["Module"].value_counts().reindex(skills, fill_value=0)
chart_df = counts.reset_index()
chart_df.columns = ["Skill", "Attempts"]
bar = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X("Skill", sort=skills, title=None),
    y=alt.Y("Attempts", title="Attempts")
)
st.altair_chart(bar)

# Improvement over time
st.subheader("Improvement over time")
for m in skills:
    sub = df[df["Module"] == m]
    if len(sub) == 0:
        continue
    if m in SCORE_SKILLS:
        st.write(f"**{m}: score % per attempt** (average {int(sub['Score %'].mean())}%)")
        chart = sub[["Score %"]].reset_index(drop=True)
    else:
        st.write(f"**{m}: grammar issues per attempt** (fewer is better)")
        chart = sub[["Grammar issues"]].reset_index(drop=True)
    chart.index = chart.index + 1
    st.line_chart(chart)

# Where to focus next
st.subheader("Where to focus next")
focus = []
for m in skills:
    sub = df[df["Module"] == m]
    if len(sub) == 0:
        focus.append(f"You have not tried **{m}** yet. Give it a go.")
    elif m in SCORE_SKILLS and sub["Score %"].mean() < 70:
        focus.append(f"Your {m} average is below 70%. Practise a few more {m.lower()} exercises.")
    elif m not in SCORE_SKILLS and sub["Grammar issues"].mean() > 2:
        focus.append(f"Your {m} attempts average more than 2 grammar issues. Slow down and check each sentence.")

if focus:
    for f in focus:
        st.markdown(f"- {f}")
else:
    st.success("Great work! Keep practising to stay consistent.")

# History table, newest first
st.subheader("Practice history")
st.dataframe(df[["Time", "Module", "Result"]].iloc[::-1], hide_index=True)
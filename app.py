import glob

import pandas as pd
import streamlit as st

st.set_page_config(page_title="BML Checker", layout="centered")
st.title("BML Checker Results")

files = sorted(glob.glob("bml_results_*.csv"))
uploads = st.file_uploader("Upload result CSVs", type="csv", accept_multiple_files=True)
chosen = st.multiselect("Or pick local files", files, default=files[:1])

frames = []
for src in list(uploads) + chosen:
    try:
        frames.append(pd.read_csv(src, dtype=str, on_bad_lines="skip").fillna(""))
    except Exception:
        continue

if not frames:
    st.info("No data loaded.")
    st.stop()

df = pd.concat(frames, ignore_index=True)
phone_cols = [c for c in df.columns if "phone" in c.lower() or "mobile" in c.lower()]

q = st.text_input("Search CNIC or phone", placeholder="e.g. 42101311811").replace("-", "").replace(" ", "")
mode = st.radio("Match", ["Contains", "Starts with", "Ends with"], horizontal=True)
statuses = sorted(df["Status"].unique()) if "Status" in df else []
status = st.multiselect("Status", statuses)

if status:
    df = df[df["Status"].isin(status)]
if q:
    mask = pd.Series(False, index=df.index)
    for col in ["CNIC"] + phone_cols:
        if col in df:
            s = df[col].str.replace(r"[\s-]", "", regex=True)
            if mode == "Contains":
                mask |= s.str.contains(q, regex=False)
            elif mode == "Starts with":
                mask |= s.str.startswith(q)
            else:
                mask |= s.str.endswith(q)
    df = df[mask]

st.caption(f"{len(df)} records")
st.dataframe(df, use_container_width=True)
st.download_button("Download filtered CSV", df.to_csv(index=False), "filtered.csv", "text/csv")

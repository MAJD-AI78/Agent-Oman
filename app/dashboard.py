import pandas as pd
import streamlit as st
import plotly.express as px

def render_dashboard(file):
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

    st.subheader("📊 Visual Insights")
    st.write(df)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols, index=1)
        fig = px.scatter(df, x=x, y=y, title="Custom Chart")
        st.plotly_chart(fig)
import streamlit as st
import pandas as pd

st.title("📊 Results Comparison")
st.markdown("Comparison between Computed, Measured, and ABC Optimized Results")
st.markdown("---")

# ------------------ CHECK ------------------
required_keys = ["abc_best_pmax", "abc_pmax_meas", "Pmax_calculated"]
missing = [k for k in required_keys if k not in st.session_state]

if missing:
    st.warning("⚠ Please run the optimizer first.")
    st.stop()

# ------------------ VALUES ------------------
Pmax_measured = st.session_state["abc_pmax_meas"]
Pmax_computed = st.session_state["Pmax_calculated"]
Pmax_optimized = st.session_state["abc_best_pmax"]

# ------------------ ERROR ------------------
error_computed = abs(Pmax_computed - Pmax_measured)
error_optimized = abs(Pmax_optimized - Pmax_measured)

# ------------------ DISPLAY ------------------
st.subheader("⚡ Pmax Comparison")

col1, col2, col3 = st.columns(3)

col1.metric("Measured (W)", f"{Pmax_measured:.4f}")
col2.metric("Computed (Before ABC)", f"{Pmax_computed:.4f}")
col3.metric("Optimized (After ABC)", f"{Pmax_optimized:.4f}")

st.markdown("---")

# ------------------ ERROR COMPARISON ------------------
st.subheader("📉 Error Comparison")

col4, col5 = st.columns(2)

col4.metric(
    "Error (Computed vs Measured)",
    f"{error_computed:.4f} W"
)

col5.metric(
    "Error (Optimized vs Measured)",
    f"{error_optimized:.4f} W",
    delta=f"{error_optimized - error_computed:.4f} W",
    delta_color="inverse"   # 🔥 makes smaller error GREEN
)

# ------------------ TABLE ------------------
st.markdown("---")
st.subheader("📋 Summary Table")

df = pd.DataFrame({
    "Type": ["Measured", "Computed", "Optimized"],
    "Pmax (W)": [Pmax_measured, Pmax_computed, Pmax_optimized],
})

st.table(df)

# ------------------ GRAPH ------------------
st.markdown("---")
st.subheader("📊 Visual Comparison")

df_chart = df.set_index("Type")
st.bar_chart(df_chart)

# ------------------ CLEAR MESSAGE ------------------
st.markdown("---")
if error_optimized < error_computed:
    st.success("✅ ABC Optimization successfully reduced the error. Optimized result is closer to measured value.")
else:
    st.error("⚠ Optimization did not improve the result. Further tuning required.")

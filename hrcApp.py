import streamlit as st
import plotly.express as px
from humanAIWorkCellEvaluator import WorkCellSimulation

#page setup
st.set_page_config(page_title="Human AI Work Cell Evaluator", layout="wide")

#title and description
st.title("Human–AI Workcell Evaluator")
st.caption("Industry 5.0 Human-Centric Decision Simulation")

#slide bar configuration
st.sidebar.header("Simulation Settings")


p_machine = st.sidebar.slider("Machine Accuracy", 0.5, 1.0, 0.85)
p_human = st.sidebar.slider("Human Accuracy", 0.5, 1.0, 0.95)
t_machine = st.sidebar.slider("Machine Cycle Time (sec)", 0.1, 2.0, 1.0)
t_override = st.sidebar.slider("Human Override Time (sec)", 0.1, 2.0, 0.5)
uncertainty_threshold = st.sidebar.slider("Human Override Threshold", 0.01, 0.5, 0.15)
noise = st.sidebar.slider("Noise Level", 0.0, 0.25, 0.05)
n_parts = st.sidebar.slider("Number of Parts", 20, 1000, 200)


#run simulation
run = st.button("Run Simulation")

if run:
    df_machine = sim.simulate_machine_only()
    df_human = sim.simulate_human_in_loop()

    #KPI calculations
    def kpis(df):
        return{
            "Accuracy": df["correct"].mean(),
            "Avg Cycle Time": df["cycle_time"].mean(),
            "Throughput (parts/min)": 60 / df["cycle_time"].mean(),
            "Intervention Rate": df["human_intervention"].mean()
        }
    
    kpi_m = kpis(df_machine)
    kpi_h = kpis(df_human)

#display results

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Machine-Only KPIs")
        st.json(kpi_m)

    with col2:
        st.subheader("Human-in-the-Loop KPIs")
        st.json(kpi_h)

    st.subheader("Accuracy Comparison")
    fig_acc = px.bar(
        x=["Machine Only", "Human in Loop"],
        y=[kpi_m["Accuracy"], kpi_h["Accuracy"]],
        labels={"x": "Mode", "y": "Accuracy"},
        title="Decision Accuracy Comparison"
    )
    st.plotly_chart(fig_acc)

    st.subheader("Throughput Comparison")
    fig_thr = px.bar(
        x=["Machine Only", "Human in Loop"],
        y=[kpi_m["Throughput (parts/min)"], kpi_h["Throughput (parts/min)"]],
        labels={"x": "Mode", "y": "Throughput"},
        title="Throughput Comparison"
    )
    st.plotly_chart(fig_thr)

    st.subheader("Intervention Rate (Human in Loop)")
    fig_int = px.bar(
        x=["Human Intervention"],
        y=[kpi_h["Intervention Rate"]],
        labels={"x": "Metric", "y": "Rate"},
        title="Human Intervention Rate"
    )
    st.plotly_chart(fig_int)
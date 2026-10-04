"""
Movementam Dynamics Web Application
Author: Noman Ali Qazi (ORCID: 0009-0006-8858-1357)
License: Apache 2.0
Description: Interactive web tool for calculating, plotting, and analyzing
             Movementam dynamics, temporal wear decay, and spatial vector telemetry.
"""

import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as rx
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Movementam Dynamics Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for executive academic formatting
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_dict_attachment=True,
)


# ==========================================
# CORE CALCULATION ENGINE
# ==========================================
class MovementamEngine:

    @staticmethod
    def compute_movementam(
        mass: float, velocity: float, area: float
    ) -> float:
        """Calculates initial Movementam (kg/(m²·s))."""
        if area <= 0:
            return 0.0
        return (mass * velocity) / area

    @staticmethod
    def compute_temporal_decay(
        initial_val: float, wear_factor: float, time_steps: np.ndarray
    ) -> np.ndarray:
        """Calculates exponential decay over time: l_m(t) = Movementam * e^(-λt)."""
        return initial_val * np.exp(-wear_factor * time_steps)

    @staticmethod
    def compute_force_and_energy(
        movementam_val: float, area: float, velocity: float, delta_t: float
    ):
        """Derives thrust vector and kinetic energy flux."""
        momentum = movementam_val * area
        thrust_force = momentum / delta_t if delta_t > 0 else 0.0
        kinetic_energy = 0.5 * momentum * velocity
        return thrust_force, kinetic_energy


# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.image(
    "https://img.shields.io/badge/ORCID-0009--0006--8858--1357-green.svg",
    use_container_width=False,
)
st.sidebar.title("System Parameters")

st.sidebar.subheader("1. Core Inputs")
mass_input = st.sidebar.number_input(
    "System Mass M (kg)", min_value=0.1, value=150.0, step=10.0
)
velocity_input = st.sidebar.number_input(
    "Velocity V (m/s)", min_value=0.1, value=1200.0, step=50.0
)
area_input = st.sidebar.number_input(
    "Aperture Area A (m²)", min_value=0.01, value=0.75, step=0.05
)

st.sidebar.subheader("2. Temporal & Wear Dynamics")
wear_lambda = st.sidebar.slider(
    "Attenuation Coefficient (λ)",
    min_value=0.000,
    max_value=0.100,
    value=0.015,
    step=0.001,
    format="%.3f",
)
time_horizon = st.sidebar.slider(
    "Time Horizon (seconds)", min_value=5, max_value=200, value=60, step=5
)
delta_t_input = st.sidebar.number_input(
    "Time Interval Δt (s)", min_value=0.001, value=1.0, step=0.1
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 **Noman Ali Qazi**")
st.sidebar.caption("Apache 2.0 Open Source License")


# ==========================================
# MAIN INTERFACE
# ==========================================
st.markdown(
    '<div class="main-header">Movementam Dynamics Engine</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Architectural Telemetry & Kinetic Systems Simulation Platform</div>',
    unsafe_allow_html=True,
)

# Calculations
engine = MovementamEngine()
base_mvm = engine.compute_movementam(mass_input, velocity_input, area_input)
thrust_f, kinetic_e = engine.compute_force_and_energy(
    base_mvm, area_input, velocity_input, delta_t_input
)

time_array = np.linspace(0, time_horizon, 200)
decay_curve = engine.compute_temporal_decay(base_mvm, wear_lambda, time_array)
final_mvm = decay_curve[-1]

# Display Top KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Initial Movementam",
        value=f"{base_mvm:,.2f}",
        delta="kg / (m²·s)",
    )
with col2:
    st.metric(
        label=f"Retained at t={time_horizon}s",
        value=f"{final_mvm:,.2f}",
        delta=f"-{((1 - final_mvm/base_mvm)*100):.1f}%",
        delta_color="inverse",
    )
with col3:
    st.metric(
        label="Derived Thrust (F)", value=f"{thrust_f:,.2f}", delta="N (Newton)"
    )
with col4:
    st.metric(
        label="Kinetic Energy Flux",
        value=f"{(kinetic_e/1e3):,.2f}",
        delta="kJ",
    )

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    ["📈 Temporal Decay Analysis", "📊 Comparative Scenarios", "ℹ️ Mathematical Reference"]
)

# ------------------------------------------
# TAB 1: TEMPORAL DECAY
# ------------------------------------------
with tab1:
    st.subheader("Temporal Kinetic Degradation Curve")

    # Interactive Plotly Chart
    fig_decay = rx.Figure()
    fig_decay.add_trace(
        rx.Scatter(
            x=time_array,
            y=decay_curve,
            mode="lines",
            name="Movementam l_m(t)",
            line=dict(color="#2563EB", width=3),
            hovertemplate="Time: %{x:.1f} s<br>Movementam: %{y:.2f} kg/(m²·s)<extra></extra>",
        )
    )

    fig_decay.update_layout(
        title="Movementam Attenuation Over Time ($l_m = e^{-\\lambda t}$)",
        xaxis_title="Time t (seconds)",
        yaxis_title="Movementam Flux Density (kg / (m²·s))",
        template="plotly_white",
        height=450,
        hovermode="x unified",
    )

    st.plotly_chart(fig_decay, use_container_width=True)

    # Telemetry Data Table
    st.subheader("Snapshot Telemetry Data")
    step_indices = np.linspace(0, len(time_array) - 1, 10, dtype=int)
    telemetry_df = pd.DataFrame(
        {
            "Time (s)": time_array[step_indices],
            "Movementam (kg/(m²·s))": decay_curve[step_indices],
            "Thrust Force (N)": (
                decay_curve[step_indices] * area_input / delta_t_input
            ),
            "Retention Ratio (%)": (decay_curve[step_indices] / base_mvm)
            * 100,
        }
    )
    st.dataframe(
        telemetry_df.style.format(
            {
                "Time (s)": "{:.1f}",
                "Movementam (kg/(m²·s))": "{:,.2f}",
                "Thrust Force (N)": "{:,.2f}",
                "Retention Ratio (%)": "{:.2f}%",
            }
        ),
        use_container_width=True,
    )

# ------------------------------------------
# TAB 2: SCENARIO COMPARISON
# ------------------------------------------
with tab2:
    st.subheader("Multi-Aperture Scenario Sensitivity Analysis")
    st.write(
        "Compare how variations in cross-sectional aperture area ($A$) affect initial flux and decay rates."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        area_mult_1 = st.slider(
            "Scenario 1 Area Multiplier", 0.2, 2.0, 0.5, 0.1
        )
    with col_b:
        area_mult_2 = st.slider(
            "Scenario 2 Area Multiplier", 0.2, 2.0, 1.5, 0.1
        )

    a1 = area_input * area_mult_1
    a2 = area_input * area_mult_2

    mvm1 = engine.compute_movementam(mass_input, velocity_input, a1)
    mvm2 = engine.compute_movementam(mass_input, velocity_input, a2)

    curve1 = engine.compute_temporal_decay(mvm1, wear_lambda, time_array)
    curve2 = engine.compute_temporal_decay(mvm2, wear_lambda, time_array)

    fig_comp = rx.Figure()
    fig_comp.add_trace(
        rx.Scatter(
            x=time_array,
            y=decay_curve,
            name=f"Baseline (A = {area_input:.2f} m²)",
            line=dict(color="#2563EB", width=2),
        )
    )
    fig_comp.add_trace(
        rx.Scatter(
            x=time_array,
            y=curve1,
            name=f"Constricted (A = {a1:.2f} m²)",
            line=dict(color="#DC2626", width=2, dash="dash"),
        )
    )
    fig_comp.add_trace(
        rx.Scatter(
            x=time_array,
            y=curve2,
            name=f"Expanded (A = {a2:.2f} m²)",
            line=dict(color="#16A34A", width=2, dash="dot"),
        )
    )

    fig_comp.update_layout(
        title="Aperture Area Impact on Movementam Telemetry",
        xaxis_title="Time t (seconds)",
        yaxis_title="Movementam Flux Density (kg / (m²·s))",
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(fig_comp, use_container_width=True)

# ------------------------------------------
# TAB 3: MATHEMATICAL REFERENCE
# ------------------------------------------
with tab3:
    st.subheader("Architectural Formulation")
    st.latex(r"L_m = \frac{M \cdot V}{A}")
    
    st.subheader("Temporal Wear Attenuation")
    st.latex(r"l_m(t) = L_m \cdot e^{-\lambda t}")
    st.markdown(
        """
        - **$\lambda$**: Wear/attenuation factor ($s^{-1}$)
        - **$t$**: Time elapsed ($s$)
        """
    )
    
    st.subheader("Derived Vector Quantities")
    st.latex(r"F = \frac{L_m \cdot A}{\Delta t}")
    st.latex(r"E_k = \frac{1}{2} (L_m \cdot A \cdot v^2)")

st.markdown("---")
st.caption(
    "Published under Apache License 2.0 by **Noman Ali Qazi**"
)


    st.subheader("Architectural Formulation")
    st.latex(r"\text{Movementam} = \frac{M \cdot V}{A}")
    st.subheader("Derived Vector Quantities")
    st.latex(r"F = \frac{L_m \cdot A}{\Delta t}")
    st.latex(r"E_k = \frac{1}{2} (L_m \cdot A \cdot v^2)")

    st.markdown(
        """
    - **$M$**: Mass of the system ($\text{kg}$)
    - **$V$**: Exhaust/Particle velocity ($\text{m/s}$)
    - **$A$**: Cross-sectional aperture area ($\text{m}^2$)
    """
    )

    st.subheader("Temporal Wear Attenuation")
    st.latex(r"l_m(t) = \text{Movementam} \cdot e^{-\lambda t}")
    st.markdown(
        """
    - **$\lambda$**: Wear/attenuation factor ($s^{-1}$)
    - **$t$**: Time elapsed ($s$)
    """
    )

    st.subheader("Derived Vector Quantities")
    st.latex(r"F = \frac{\text{Movementam} \cdot A}{\Delta t}")
    st.latex(r"E_k = \frac{1}{2} (\text{Movementam} \cdot A \cdot V)")

    st.markdown("---")
    st.caption(
        "Published under Apache License 2.0 by **Noman Ali Qazi** | ORCID: [0009-0006-8858-1357](https://orcid.org/0009-0006-8858-1357)"
    )
    

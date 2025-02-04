import numpy as np
import pandas as pd
import streamlit as st

def calculate_lcoh(capex, opex, efficiency, wacc, lifetime, energy_price):
    """Compute the Levelized Cost of Hydrogen (LCOH) in $/kg."""
    capital_recovery_factor = (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)
    fixed_costs = capex * capital_recovery_factor + opex
    variable_costs = energy_price / efficiency
    return fixed_costs + variable_costs

def calculate_transport_costs(distance, mode):
    """Compute hydrogen transportation costs based on distance (km) and transport mode."""
    transport_modes = {
        "pipeline_new": 0.64,  # $/1000 km/kg H2
        "pipeline_retrofit": 0.13,
        "shipping_LH2": 1.5,  # $/1000 km/kg H2
    }
    return (distance / 1000) * transport_modes.get(mode, 0)

# Streamlit UI
st.title("Hydrogen Cost Calculator")

country = st.text_input("Enter Country:")
capex = st.number_input("CAPEX ($/kW):", min_value=0.0, value=900.0)
opex = st.number_input("OPEX ($/kW-year):", min_value=0.0, value=20.0)
efficiency = st.number_input("Efficiency (0-1):", min_value=0.0, max_value=1.0, value=0.66)
wacc = st.number_input("WACC (%):", min_value=0.0, max_value=1.0, value=0.08)
lifetime = st.number_input("Lifetime (years):", min_value=1, value=25)
energy_price = st.number_input("Energy Price ($/MWh):", min_value=0.0, value=50.0)
transport_distance = st.number_input("Transport Distance (km):", min_value=0.0, value=2000.0)
transport_mode = st.selectbox("Transport Mode:", ["pipeline_new", "pipeline_retrofit", "shipping_LH2"])

if st.button("Calculate"):
    lcoh = calculate_lcoh(capex, opex, efficiency, wacc, lifetime, energy_price)
    transport_costs = calculate_transport_costs(transport_distance, transport_mode)
    total_cost = lcoh + transport_costs
    
    st.write(f"### Results for {country}")
    st.write(f"**LCOH:** ${lcoh:.2f}/kg")
    st.write(f"**Transport Cost:** ${transport_costs:.2f}/kg")
    st.write(f"**Total Cost:** ${total_cost:.2f}/kg")

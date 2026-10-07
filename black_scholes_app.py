import streamlit as st
import numpy as np
import yfinance as yf  # Added for live global market data feeds
from math import log, sqrt, exp
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📈",
    layout="wide",
)

# ---------------- HEADER ----------------
st.title("📈 Black-Scholes Option Pricing Dashboard")
st.caption("Developed by Issac Qaiser • Live Market Feeds • Payoff • Greeks • IV Scanner • Heatmaps")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("Live Market Data Feed")

# Interactive ticker lookup text input
ticker_input = st.sidebar.text_input("Stock Ticker Symbol", value="AAPL").upper().strip()

# Background API data fetch engine
live_price = 100.0
if ticker_input:
    try:
        ticker_data = yf.Ticker(ticker_input)
        # Safely pull the most recent closing price from the live global market feed
        todays_data = ticker_data.history(period="1d")
        if not todays_data.empty:
            live_price = float(todays_data['Close'].iloc[-1])
            st.sidebar.success(f"Live {ticker_input} Price: ${live_price:.2f}")
        else:
            st.sidebar.warning("Ticker not found. Using default baseline.")
    except Exception:
        st.sidebar.warning("API timeout or invalid ticker. Using default baseline.")

st.sidebar.header("Underlying & Model Parameters")
S = st.sidebar.number_input("Current Asset Price (S)", value=live_price, min_value=0.0001)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.0001)
T = st.sidebar.number_input("Time to Maturity (Years)", value=1.0, min_value=0.0001)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.25, min_value=0.0001)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)

st.sidebar.header("Premium & Position")
premium = st.sidebar.number_input("Premium Paid/Received", value=10.0)
position = st.sidebar.selectbox("Position Type", ["Long Call", "Short Call", "Long Put", "Short Put"])

st.sidebar.header("IV Scanner Inputs")
market_call = st.sidebar.number_input("Market Call Price", value=10.0, min_value=0.0001)
market_put = st.sidebar.number_input("Market Put Price", value=10.0, min_value=0.0001)

st.sidebar.header("Payoff Diagram Range")
payoff_min = st.sidebar.number_input("Min Spot (Payoff)", value=50.0)
payoff_max = st.sidebar.number_input("Max Spot (Payoff)", value=150.0)

st.sidebar.header("Heatmap Settings")
spot_min_heat = st.sidebar.number_input("Min Spot (Heatmap)", value=80.0)
spot_max_heat = st.sidebar.number_input("Max Spot (Heatmap)", value=120.0)
vol_min = st.sidebar.number_input("Min Vol (Heatmap)", value=0.10)
vol_max = st.sidebar.number_input("Max Vol (Heatmap)", value=0.30)
grid = st.sidebar.slider("Grid Resolution", 20, 50, 30)

# ---------------- BLACK-SCHOLES CORE ENGINE ----------------
def bs(S, K, T, sigma, r):
    d1 = (log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)

    call = S*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
    put = K*exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    return {
        "call": call,
        "put": put,
        "delta_c": norm.cdf(d1),
        "delta_p": norm.cdf(d1) - 1,
        "gamma": norm.pdf(d1) / (S*sigma*sqrt(T)),
        "vega": S * norm.pdf(d1) * sqrt(T),
        "theta_c": -S*norm.pdf(d1)*sigma/(2*sqrt(T)) - r*K*exp(-r*T)*norm.cdf(d2),
        "theta_p": -S*norm.pdf(d1)*sigma/(2*sqrt(T)) + r*K*exp(-r*T)*norm.cdf(-d2),
        "rho_c": K*T*exp(-r*T)*norm.cdf(d2),
        "rho_p": -K*T*exp(-r*T)*norm.cdf(-d2),
    }

res = bs(S, K, T, sigma, r)

# ---------------- FIXED IV SCANNER FUNCTIONS ----------------
def implied_vol_call(S, K, T, r, market_price):
    sigma_est = 0.2
    for _ in range(100):
        res_bs = bs(S, K, T, sigma_est, r)
        diff = res_bs["call"] - market_price
        if abs(diff) < 1e-6: 
            return sigma_est
        v = res_bs["vega"]
        if abs(v) < 1e-6: 
            break
        sigma_est -= diff / v
    return max(sigma_est, 0.0)

def implied_vol_put(S, K, T, r, market_price):
    sigma_est = 0.2
    for _ in range(100):
        res_bs = bs(S, K, T, sigma_est, r)
        diff = res_bs["put"] - market_price
        if abs(diff) < 1e-6: 
            return sigma_est
        v = res_bs["vega"]
        if abs(v) < 1e-6: 
            break
        sigma_est -= diff / v
    return max(sigma_est, 0.0)

def iv_label(iv):
    if iv <= 0.001:
        return "N/A (Theoretical Error) ⚪", "gray"
    elif iv < 0.15:
        return "LOW 🟢", "green"
    elif iv < 0.35:
        return "NORMAL 🟠", "orange"
    else:
        return "HIGH 🔴", "red"

# ---------------- TOP METRICS PANEL ----------------
col1, col2 = st.columns(2)
col1.success(f"CALL Value: ${res['call']:.2f}")
col2.error(f"PUT Value: ${res['put']:.2f}")

# ---------------- P&L TRACKING ----------------
st.subheader("P&L Tracking")

model_price = res["call"] if "Call" in position else res["put"]
sign = 1 if "Long" in position else -1
pnl = sign * (model_price - premium)

if pnl > 0:
    pnl_text = "Profit"
    pnl_arrow = "↑"
    pnl_color = "green"
elif pnl < 0:
    pnl_text = "Loss"
    pnl_arrow = "↓"
    pnl_color = "red"
else:
    pnl_text = "Break-even"
    pnl_arrow = "→"
    pnl_color = "gray"

col1, col2, col3 = st.columns(3)
col1.metric("Model Price", f"${model_price:.2f}")
col2.metric("Premium", f"${premium:.2f}")
col3.metric("P&L", f"${pnl:.2f}")
col3.markdown(f"<span style='color:{pnl_color}; font-weight:bold;'>{pnl_text} {pnl_arrow}</span>", unsafe_allow_html=True)

# ---------------- PAYOFF DIAGRAM ----------------
st.subheader("Payoff Diagram")

spots = np.linspace(payoff_min, payoff_max, 200)
payoff = []

for s in spots:
    if "Call" in position:
        intrinsic = max(s - K, 0)
    else:
        intrinsic = max(K - s, 0)
    payoff.append(sign * (intrinsic - premium))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(spots, payoff, color="blue", lw=2)
ax.axhline(0, color="gray", linewidth=1, linestyle="--")
ax.set_xlabel("Spot Price")
ax.set_ylabel("P&L")
ax.set_title(f"Payoff Diagram • {position}")
st.pyplot(fig)

# ---------------- GREEKS MATRIX ----------------
st.subheader("Greeks")

g1, g2, g3, g4 = st.columns(4)
g1.metric("Delta (Call)", f"{res['delta_c']:.4f}")
g1.metric("Delta (Put)", f"{res['delta_p']:.4f}")
g2.metric("Gamma", f"{res['gamma']:.6f}")
g3.metric("Vega", f"{res['vega']:.6f}")
g4.metric("Theta (Call)", f"{res['theta_c']:.4f}")
g4.metric("Theta (Put)", f"{res['theta_p']:.4f}")

g5, g6 = st.columns(2)
g5.metric("Rho (Call)", f"{res['rho_c']:.4f}")
g6.metric("Rho (Put)", f"{res['rho_p']:.4f}")

# ---------------- IV SCANNER PANEL ----------------
st.subheader("Implied Volatility Scanner")

iv_call = implied_vol_call(S, K, T, r, market_call)
iv_put = implied_vol_put(S, K, T, r, market_put)

call_label, call_color = iv_label(iv_call)
put_label, put_color = iv_label(iv_put)

ivc, ivp = st.columns(2)
display_call_iv = f"{iv_call:.4f}" if iv_call > 0.001 else "N/A"
display_put_iv = f"{iv_put:.4f}" if iv_put > 0.001 else "N/A"

ivc.markdown(f"<h4>Call IV: <span style='color:{call_color}; font-weight:bold;'>{display_call_iv} ({call_label})</span></h4>", unsafe_allow_html=True)
ivp.markdown(f"<h4>Put IV: <span style='color:{put_color}; font-weight:bold;'>{display_put_iv} ({put_label})</span></h4>", unsafe_allow_html=True)

# ----------------  MATRIX HEATMAPS ----------------
st.subheader("Option Price Heatmaps")

spot_grid = np.linspace(spot_min_heat, spot_max_heat, grid)
vol_grid = np.linspace(vol_min, vol_max, grid)

call_map = np.zeros((grid, grid))
put_map = np.zeros((grid, grid))

for i, s_ in enumerate(spot_grid):
    for j, v_ in enumerate(vol_grid):
        r_ = bs(s_, K, T, v_, r)
        call_map[j, i] = r_["call"]
        put_map[j, i] = r_["put"]

x_labels = [f"{x:.1f}" for x in spot_grid]
y_labels = [f"{y:.2f}" for y in vol_grid]
stride = max(1, grid // 5)

hc, hp = st.columns(2)

with hc:
    st.write("### Call Price Heatmap")
    fig_c, ax_c = plt.subplots(figsize=(6, 4.5))
    sns.heatmap(call_map, cmap="Greens", ax=ax_c, xticklabels=x_labels, yticklabels=y_labels)
    ax_c.invert_yaxis() 
    ax_c.set_xticks(ax_c.get_xticks()[::stride])
    ax_c.set_xticklabels(x_labels[::stride])
    ax_c.set_yticks(ax_c.get_yticks()[::stride])
    ax_c.set_yticklabels(y_labels[::stride])
    ax_c.set_xlabel("Spot Price")
    ax_c.set_ylabel("Volatility (σ)")
    st.pyplot(fig_c)

with hp:
    st.write("### Put Price Heatmap")
    fig_p, ax_p = plt.subplots(figsize=(6, 4.5))
    sns.heatmap(put_map, cmap="Reds", ax=ax_p, xticklabels=x_labels, yticklabels=y_labels)
    ax_p.invert_yaxis() 
    ax_p.set_xticks(ax_p.get_xticks()[::stride])
    ax_p.set_xticklabels(x_labels[::stride])
    ax_p.set_yticks(ax_p.get_yticks()[::stride])
    ax_p.set_yticklabels(y_labels[::stride])
    ax_p.set_xlabel("Spot Price")
    ax_p.set_ylabel("Volatility (σ)")
    st.pyplot(fig_p)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Black-Scholes Dashboard • Live Market Feeds • Payoff • Greeks • IV Scanner • Heatmaps")
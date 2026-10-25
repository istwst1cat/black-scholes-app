# Black-Scholes-Merton Options Analytics Engine

An independent quantitative finance dashboard engineered from scratch to evaluate European-style derivative structures under live market conditions using Python, `yfinance`, and custom numerical solvers.

## Core Technical Features

* **Live Market Data:** Integrates `yfinance` to pull real-time spot metrics into the pricing loop.
* **Vectorized Valuation:** Consolidates option formulas into a vectorized function layer to prevent lag.
* **Newton-Raphson Solver:** Reconstructs market volatility expectations using iterative optimization with convergence guards.
* **Risk Matrices:** Maps discrete spot price movements against shifts in volatility (\(\sigma\)).

## The Mathematical Framework

The engine models asset coordinates assuming a log-normal distribution:
```math
d1 = (ln(S0 / K) + (r + (sigma^2) / 2) * T) / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```
 
### Pricing & Greeks
Calculates theoretical premiums (Call/Put) and partial derivatives for Delta, Gamma, Vega, Theta, and Rho using standard normal distribution statistics.

## Runtime Protection & Execution

Includes a conditional check against division-by-zero errors when Vega collapses in deep out-of-the-money states:
```python
v = res_bs["vega"]
if abs(v) < 1e-6:
    break 
```

## Dependencies & Launch
Utilizes `streamlit`, `numpy`, `scipy`, `matplotlib`, `seaborn`, and `yfinance`. Run via terminal:
```bash
streamlit run black_scholes_app.py
```

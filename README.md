# 📈 Black-Scholes-Merton Options Analytics Engine 
### *The Independent "Quant Trader Starter Kit" Portfolio Highlight*

An institutional-grade, production-optimized quantitative finance engine and risk simulation dashboard built completely from scratch. This standalone terminal evaluates European-style derivative structures, computes high-precision risk vulnerabilities (the Greeks), extracts implied parameters via numerical methods, and models multi-dimensional risk matrices across live assets.

Developed independently by **Issac Qaiser** as a cornerstone portfolio display for university evaluation.

---

## 🎯 Architecture & Technical Core

This dashboard bridges foundational stochastic calculus paradigms with modern data engineering design patterns to remove idealize textbook constraints and calculate accurate risk parameters under live market dynamics:

*   **Live Market Data Feed Integration:** Pipelines external data structures using the `yfinance` API framework to extract real-time underlying global spot metrics (`S`) and display dynamic success indicators.
*   **Vectorized Parameter Caching Engine:** Consolidates analytical options evaluations (`Call`/`Put`) directly into a centralized master function loop. This limits computational overhead and prevents array lagging when execution matrices are expanded.
*   **Numerical Implied Volatility Solver:** Reconstructs unobservable market expectations using an iterative **Newton-Raphson optimization routine** with absolute exception limits to prevent mathematical crash loops.
*   **Multidimensional Risk Mesh Matrix:** Generates automated two-dimensional meshes mapping discrete changes in stock prices against shifting volatility coefficients (`σ`) using dynamically scaled stride constraints.

---

## 📊 The Mathematical Framework

The pricing engine continuously models asset coordinates assuming a log-normal distribution path, discounting continuous discounting fields safely:

\[d_1 = \frac{\ln(S_0 / K) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}}\]

\[d_2 = d_1 - \sigma \sqrt{T}\]

### Exact Pricing Equations:
*   **Call Theoretical Premium (C):**  \(C = S_0 N(d_1) - K e^{-rT} N(d_2)\)
*   **Put Theoretical Premium (P):**   \(P = K e^{-rT} N(-d_2) - S_0 N(-d_1)\)

*Where N(x) represents the standard normal Cumulative Distribution Function (CDF) compiled via specialized statistical library metrics.*

### Analytical Derivatives (Risk Greeks Engine):
The app calculates structural system sensitivities natively using the Probability Density Function height metrics (n(x)) of the standard curve:
*   **Delta (Δ):** Measures price exposure speed. \(\Delta_{Call} = N(d_1)\) | \(\Delta_{Put} = N(d_1) - 1\)
*   **Gamma (Γ):** Evaluates stability acceleration. \(\Gamma = \frac{n(d_1)}{S_0 \sigma \sqrt{T}}\)
*   **Vega (\(\mathcal{V}\)):** Tracks variance sensitivity to a 1% shift in σ. \(\mathcal{V} = S_0 n(d_1) \sqrt{T}\)
*   **Theta (Θ):** Models structural time decay premium.
*   **Rho (ρ):** Captures macroeconomic risk sensitivity to interest rate movements (r).

---

## 🧠 Numerical Method Optimization: The IV Scanner

Because implied volatility (σ) cannot be extracted algebraically from the Black-Scholes formula, this dashboard uses a custom **Newton-Raphson approximation solver** to isolate the true root through rapid derivative cycles:

\[\sigma_{n+1} = \sigma_n - \frac{C_{Model}(\sigma_n) - C_{Market}}{\mathcal{V}(\sigma_n)}\]

### 🔒 Operational Resilience & Failsafe Guards
Standard student models fall apart in deep out-of-the-money states because the derivative denominator (**Vega**) collapses toward zero, triggering terminal runtime errors. This engine embeds a defensive conditional boundary check:
```python
v = res_bs["vega"]
if abs(v) < 1e-6: 
    break  # Defends system thread against division-by-zero crashes
```
If convergence limits are violated by anomalous input numbers, the function triggers automated fallback boundaries (`max(sigma_est, 0.0)`) ensuring system stability.

---

## 📦 System Dependencies & Requirements

To launch the dashboard locally, your runtime environment requires these specific data science libraries:

*   **`streamlit`** - Renders the asynchronous interactive user dashboard frontend framework.
*   **`numpy`** - Manages fast, multidimensional array processes and vectorized matrix math.
*   **`scipy`** - Compiles exact cumulative distribution statistics for standard curve modeling.
*   **`matplotlib`** - Architectures basic visual canvases and graph templates.
*   **`seaborn`** - Formats the refined color matrix heatmaps (Greens/Reds risk scales).
*   **`yfinance`** - Houses the background network connections to live Wall Street tickers.

Create a `requirements.txt` file in your root path containing:
```text
streamlit
numpy
scipy
matplotlib
seaborn
yfinance
```

---

## 🚀 Local Installation & Execution

Follow these exact steps in your terminal environment to run the application live:

1. **Clone or download the project files into your folder structure:**
   ```bash
   cd path/to/your/project/folder
   ```

2. **Execute package installation to synchronize requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the engine dashboard using Streamlit:**
   ```bash
   streamlit run black_scholes_app.py
   ```
   *The script will initialize a local execution port, automatically opening the dashboard layout inside your default web browser tab.*

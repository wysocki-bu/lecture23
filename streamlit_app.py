import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Example Streamlit Visualizations (Python Code) ",
    page_icon=" ",
    layout="wide",
)

st.title("Dashboard with Example Visualizations")

# Create the 4 requested tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Simulated Stock Demo",
    "2. App Source Code",
    "3. Code Sources & Attribution",
    "4. Theory & Help",
])

# ==========================================
# TAB 1: SIMULATED STOCK PRICE DEMO
# ==========================================
with tab1:
    st.header("Geometric Brownian Motion (GBM) Stock Simulator") 
 

 
 
@st.cache_data
def load_customers():
    rng = np.random.default_rng(3)
    n = 300
    return pd.DataFrame({
        "customer": [f"Customer {i:03d}" for i in range(n)],
        "plan": rng.choice(["Basic", "Pro", "Team"], n),
        "monthly_revenue": rng.gamma(2.0, 150.0, n).round(),
        "active_users": rng.integers(1, 120, n),
    })
 
 
customers = load_customers()
 
st.title("Customers")
st.caption("Drag a box or lasso over the points to list those customers.")
fig = px.scatter(customers, x="active_users", y="monthly_revenue", hover_name="customer")
event = st.plotly_chart(fig, on_select="rerun", selection_mode=("box", "lasso"))
 
rows = event.selection.point_indices
if rows:
    st.dataframe(customers.iloc[rows], hide_index=True)
else:
    st.info("Nothing selected yet.")



# ==================================================================================
# TAB 2: (A) GITHUB LINK, (B) COLAB CODE (IF USED), (C) ACTUAL STREAMLIT PYTHON CODE
# ==================================================================================
with tab2:
    st.header("Full Application Source Code")
    st.markdown(
        "🔗 **GitHub Repository:** "
        "[https://github.com/wysocki-bu/AC420_example](https://github.com/wysocki-bu/AC420_example) "
    )
    st.info(
        "EX. 1: Below is the Python code powering this app (copied from Github Repository)."
    )

    example_code = '''        import numpy as np
        import pandas as pd
        import streamlit as st
        etc.'''         
    st.code(example_code, language="python", line_numbers=True)

    st.info(
        "EX. 2: Below is the Python code powering this app, read dynamically from Github Repository."
    )

    try:
        with open(__file__, "r", encoding="utf-8") as f:
            source_code = f.read()
        st.code(source_code, language="python", line_numbers=True)
    except Exception as e:
        st.error(f"Could not read source file automatically: {e}")


# ==========================================
# TAB 3: CODE SOURCES & ATTRIBUTION
# ==========================================
with tab3:
    st.header("Code Sources, Libraries & Attribution")
    st.markdown(
        "This application was built by combining open-source Python libraries, "
        "standard finance formulas, and AI-assisted layout assistance."
    )

    st.subheader("1. AI Assistance")
    st.markdown(
        """
        * **LLM Code Generation (Google Gemini):** Used to scaffold the multi-tab Streamlit layout.
        """
    )

    st.subheader("2. Open-Source Libraries & Documentation")
    st.markdown(
        """
        * **Streamlit (`streamlit`):** Used for the web application framework, interactive widgets 
          (`st.tabs`, `st.slider`, `st.metric`), and native charting (`st.line_chart`). 
          *Reference: [Streamlit Documentation](https://streamlit.io)*
        * **NumPy (`numpy`):** Used for vectorized pseudo-random normal distribution sampling 
          (`np.random.default_rng`) and exponential cumulative sum calculations. 
          *Reference: [NumPy Random Sampling Docs](https://numpy.org)*
        * **Pandas (`pandas`):** Used to structure the time-series arrays into labeled DataFrames 
          for tabular inspection and plotting. 
          *Reference: [Pandas Documentation](https://pydata.org)*
        """
    )

    st.subheader("3. Mathematical & Financial References")
    st.markdown(
        """
        * **Geometric Brownian Motion (GBM) Discretization:** Adapted from standard quantitative 
          finance literature (e.g., John C. Hull, *Options, Futures, and Other Derivatives*), 
          using the exact analytical solution to the stochastic differential equation rather than 
          an Euler-Maruyama approximation to prevent negative stock prices.
        """
    )


# ==========================================
# TAB 4: THEORY & HELP PAGE
# ==========================================
with tab4:
    st.header("How Stock Prices Move: The Theory Behind the Simulation")
    st.markdown(
        """
        In real financial markets, stock prices move due to supply and demand driven by earnings 
        reports, macroeconomic news, interest rates, and investor sentiment. Because new information 
        arrives unpredictably, short-term price movements appear random.
        """
    )

    st.subheader("1. The Random Walk & Geometric Brownian Motion (GBM)")
    st.markdown(
        """
        Quantitative finance commonly models stock prices as a continuous-time stochastic process 
        called **Geometric Brownian Motion (GBM)**—the same foundational assumption used in the 
        famous Black-Scholes options pricing model.

        The change in a stock's price ($dS$) over a tiny step in time ($dt$) is governed by the 
        stochastic differential equation:
        """
    )
    st.latex(r"dS_t = \mu S_t \, dt + \sigma S_t \, dW_t")

    st.markdown(
        """
        This equation breaks stock movement into two distinct forces:
        1. **Deterministic Drift ($\mu S_t \, dt$):** The predictable trend or expected growth rate 
           ($\mu$) of the stock over time (e.g., reflecting long-term company growth and inflation).
        2. **Random Shock / Diffusion ($\sigma S_t \, dW_t$):** The unpredictable daily volatility 
           ($\sigma$) scaled by a Wiener process ($dW_t$), representing random market news and noise.
        """
    )

    st.subheader("2. Exact Simulation Formula Used in Tab 1")
    st.markdown(
        """
        To simulate daily prices over discrete steps ($\Delta t = \\frac{1}{252}$ years), we apply 
        Itô's Lemma to solve the equation above:
        """
    )
    st.latex(
        r"S_{t+\Delta t} = S_t \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} \, Z \right)"
    )
    st.markdown(
        """
        * **$S_t$**: Stock price at day $t$.
        * **$\mu$**: Expected annual return (Drift).
        * **$\sigma$**: Annualized volatility (standard deviation of returns).
        * **$Z$**: A random number drawn from a standard normal distribution ($Z \sim \mathcal{N}(0, 1)$).
        * **$-\frac{1}{2}\sigma^2$**: The *Itô correction term*, which accounts for the fact that 
          volatility drags down geometric compounding (e.g., a 50% drop followed by a 50% gain leaves 
          you at 75% of your starting value, not 100%).
        """
    )

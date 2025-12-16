import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Your provided conversion function
# -----------------------------
def convert_cumulative_to_SIR(df, date_col='date', cumulative_col='cumulative_cases',
                              population=None, infectious_period=8, recovered_col=None,
                              new_case_col='new_cases', I_col='I_est', R_col='R_est', S_col='S_est'):

    df = df.copy()

    # Ensure date column sorted
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col).reset_index(drop=True)

    if cumulative_col not in df.columns:
        raise ValueError(f"Column '{cumulative_col}' not found in dataframe.")

    # Compute new cases
    df[new_case_col] = df[cumulative_col].diff().fillna(df[cumulative_col].iloc[0])
    df[new_case_col] = df[new_case_col].clip(lower=0)

    # Estimate I(t)
    df[I_col] = df[new_case_col].rolling(window=infectious_period, min_periods=1).sum()

    # Estimate R(t)
    df[R_col] = df[cumulative_col].shift(infectious_period).fillna(0)

    # Compute S(t)
    if population is not None:
        df[S_col] = population - df[I_col] - df[R_col]
        df[S_col] = df[S_col].clip(lower=0)
    else:
        df[S_col] = np.nan

    return df


# =====================================================
# 1. LOAD YOUR DATASET
# =====================================================

df = pd.read_csv("measles_nigeria_data_2020-2021_new_cases.csv")

print("Columns in file:", df.columns.tolist())

# Your columns are:
# date
# confirmed_cases
date_col = "date"
cumulative_col = "confirmed_cases"   # <--- IMPORTANT FIX


# =====================================================
# 2. CONVERT CUMULATIVE → S, I, R
# =====================================================

population = 1_000_000   # Replace with real value if you know it

df_sir = convert_cumulative_to_SIR(
    df,
    date_col=date_col,
    cumulative_col=cumulative_col,
    population=population,
    infectious_period=8,
    new_case_col="new_cases",
    I_col="I_est",
    R_col="R_est",
    S_col="S_est"
)

print(df_sir.head())


# =====================================================
# 3. PLOT S, I, R
# =====================================================

plt.figure(figsize=(12,6))
plt.plot(df_sir[date_col], df_sir["S_est"], label="Susceptible S(t)")
plt.plot(df_sir[date_col], df_sir["I_est"], label="Infected I(t)")
plt.plot(df_sir[date_col], df_sir["R_est"], label="Recovered R(t)")

plt.xlabel("Date")
plt.ylabel("Population")
plt.title("SIR Model Estimates")
plt.legend()
plt.grid(True)
plt.show()


# Optional: I(t) only
plt.figure(figsize=(12,5))
plt.plot(df_sir[date_col], df_sir["I_est"], color="red")
plt.title("Estimated Active Infections I(t)")
plt.grid(True)
plt.show()


# Optional: I(t) log scale
plt.figure(figsize=(12,5))
plt.plot(df_sir[date_col], df_sir["I_est"], color="red")
plt.yscale("log")
plt.title("I(t) on Log Scale")
plt.grid(True)
plt.show()

# =====================================================
# 4. RUN EULER'S METHOD SIR SIMULATION
# =====================================================

# Import or define your Euler SIR function here
def euler_sir(beta, gamma, S0, I0, R0, t, N):

    S = np.empty(len(t), float)
    I = np.empty(len(t), float)
    R = np.empty(len(t), float)

    S[0], I[0], R[0] = S0, I0, R0

    for n in range(len(t) - 1):
        dt = t[n + 1] - t[n]  # time step (usually = 1)

        # DIFFERENTIAL EQUATIONS
        dS = -beta * S[n] * I[n] / N
        dI = beta * S[n] * I[n] / N - gamma * I[n]
        dR = gamma * I[n]

        # EULER UPDATES
        S[n + 1] = S[n] + dt * dS
        I[n + 1] = I[n] + dt * dI
        R[n + 1] = R[n] + dt * dR

    return S, I, R


# ---- INITIAL CONDITIONS FROM YOUR DATA ----
S0 = df_sir["S_est"].iloc[0]
I0 = df_sir["I_est"].iloc[0]
R0 = df_sir["R_est"].iloc[0]

# ---- TIME ARRAY (1 step per day) ----
t = np.arange(len(df_sir))   # e.g., 0,1,2,3,... days

# ---- PARAMETERS (adjust if needed) ----
beta = 1.8     # infection rate
gamma = 1/8         # recovery rate (infectious period = 8 days)
N = population       # total population (same used earlier)

# ---- RUN EULER SIR ----
S_sim, I_sim, R_sim = euler_sir(beta, gamma, S0, I0, R0, t, N)

# =====================================================
# 5. PLOT EULER'S SIR RESULTS
# =====================================================

plt.figure(figsize=(12,6))
plt.plot(df_sir[date_col], S_sim, '--', label="Euler S(t)", linewidth=2)
plt.plot(df_sir[date_col], I_sim, '--', label="Euler I(t)", linewidth=2)
plt.plot(df_sir[date_col], R_sim, '--', label="Euler R(t)", linewidth=2)

plt.title("Euler SIR Model Simulation")
plt.xlabel("Date")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.show()

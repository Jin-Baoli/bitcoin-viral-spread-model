import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

# ==========================================================
# 1. Fetch Bitcoin historical and current data from network
# ==========================================================
print("Fetching Bitcoin historical data from Yahoo Finance...")
df = yf.download("BTC-USD", start="2010-01-01")

# Data cleaning: remove timezone info, filter out non-positive prices and drop NaNs
df.index = df.index.tz_localize(None)
if isinstance(df['Close'], pd.DataFrame):
    df['Price'] = df['Close'].iloc[:, 0]
else:
    df['Price'] = df['Close']

df = df[df['Price'] > 0].dropna()

prices = df['Price'].values
df['Days'] = (df.index - df.index[0]).days
t = df['Days'].values

# ==========================================================
# 2. Define and fit Timothy Peterson's Gompertz Model
# ==========================================================
def gompertz_log(t, A, b, c):
    """
    Logarithmic form of the Gompertz Growth Function:
    ln(P) = A - b * exp(-c * t)
    """
    return A - b * np.exp(-c * t)

# Robust initial parameter guessing
A_init = np.log(prices.max() * 5)  
b_init = A_init - np.log(prices[0]) 
c_init = 0.0005                    
p0 = [A_init, b_init, c_init]

print("Fitting data to the viral spread model...")
popt, pcov = curve_fit(gompertz_log, t, np.log(prices), p0=p0, maxfev=20000)
A_opt, b_opt, c_opt = popt

# Calculate theoretical model prices
model_prices = np.exp(gompertz_log(t, A_opt, b_opt, c_opt))
theoretical_max = np.exp(A_opt)

print("\n" + "="*50)
print("【MODEL FITTING COMPLETED】")
print(f"Theoretical Long-term Price Cap (a): ${theoretical_max:,.2f} USD")
print(f"Viral Network Spread Rate (c):       {c_opt:.6f}")
print("="*50 + "\n")

# ==========================================================
# 3. Plotting and Interactive Hover Implementation
# ==========================================================
fig, ax = plt.subplots(figsize=(12, 7))

# Plot actual prices and model line
line_actual, = ax.plot(df.index, prices, label='Actual BTC Price', color='#f2a900', alpha=0.6, linewidth=1.5)
line_model, = ax.plot(df.index, model_prices, label="Peterson's Gompertz Model", color='#1e3d59', linestyle='--', linewidth=2.5)

ax.set_yscale('log')
ax.set_title("Bitcoin Price vs. Gompertz Viral Spread Model", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Price (USD, Log Scale)", fontsize=12)
ax.grid(True, which="both", linestyle="--", alpha=0.3)
ax.legend(fontsize=11, loc='upper left')

# Create dynamic visual components for mouse hovering
v_line = ax.axvline(x=df.index[0], color='gray', linestyle=':', alpha=0.8, visible=False)
annot = ax.annotate("", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.5", fc="#ffffff", ec="gray", alpha=0.9, lw=1),
                    fontsize=10, fontfamily='monospace')
annot.set_visible(False)

# Hover event handler
def on_hover(event):
    if event.inaxes == ax:
        try:
            # Convert mouse x-coordinate back to timezone-naive datetime
            target_date = mdates.num2date(event.xdata).replace(tzinfo=None)
            
            # Find the closest matching date index in dataframe
            idx = df.index.get_indexer([target_date], method='nearest')[0]
            
            # Extract data point details
            current_date = df.index[idx].strftime('%Y-%m-%d')
            actual_val = prices[idx]
            model_val = model_prices[idx]
            
            # Update the tracking vertical line position
            v_line.set_xdata([df.index[idx]])
            v_line.set_visible(True)
            
            # Position and update the annotation text box
            annot.xy = (df.index[idx], event.ydata)
            hover_text = (
                f"Date:   {current_date}\n"
                f"Actual: ${actual_val:,.2f}\n"
                f"Model:  ${model_val:,.2f}"
            )
            annot.set_text(hover_text)
            annot.set_visible(True)
            
            # Redraw the canvas to reflect changes
            fig.canvas.draw_idle()
        except Exception:
            pass
    else:
        # Hide interactive elements when mouse leaves the plot area
        if annot.get_visible():
            annot.set_visible(False)
            v_line.set_visible(False)
            fig.canvas.draw_idle()

# Register the mouse motion event listener
fig.canvas.mpl_connect("motion_notify_event", on_hover)

plt.tight_layout()
plt.show()
# Bitcoin Gompertz Viral Spread Model

An interactive quantitative finance tool that models Bitcoin's long-term price trajectory as a biological phenomenon. Based on the seminal research paper **"Bitcoin Spreads Like a Virus"** (2019) by Timothy Peterson, this project fetches live historical data and fits it to a non-linear Gompertz growth curve using network effect mechanics.

## 📈 Theoretical Background

Unlike traditional assets, decentralized networks propagate much like biological viruses or tumor growths. This project utilizes the **Gompertz Growth Function** (an asymmetrical sigmoid curve) combined with **Metcalfe's Law** to map out Bitcoin’s structural valuation center over time, filtering out short-term speculative market noise.

The underlying math model is expressed as:

$$P(t) = a \cdot e^{-b \cdot e^{-c \cdot t}}$$

Where:
* **$a$**: The theoretical long-term price cap (asymptote).
* **$b$**: Time-axis displacement coefficient.
* **$c$**: The viral growth/infection rate coefficient of the network.

---

## ⚡ Features

* **Automated Data Pipeline**: Dynamically streams all available daily historical data of `BTC-USD` directly from Yahoo Finance API (`yfinance`).
* **Logarithmic Non-Linear Fitting**: Implements Robust SciPy least-squares optimization (`curve_fit`) adapted to logarithmic space to prevent distortion from high late-stage prices.
* **Interactive Data Visualization**: Built with an advanced custom Matplotlib engine featuring:
  * Logarithmic scaling to accurately display multiple orders of magnitude.
  * Synchronized vertical crosshair tracking.
  * **Real-time Mouse Hover Tooltip**: Hovering anywhere on the canvas dynamically outputs the Date, Actual Price, and Model Value in an elegant monospace tracking box.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed. You will need the following data science and plotting libraries:

```bash
pip install yfinance pandas numpy scipy matplotlib

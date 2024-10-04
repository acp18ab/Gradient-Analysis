import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data for glucose levels over 10 days
data = {'Date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'Glucose_Level': [90, 92, 85, 88, 94, 100, 105, 110, 108, 107]}
df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

# Calculate the gradient (rate of change per day)
df['Glucose_Gradient'] = df['Glucose_Level'].diff() / df.index.to_series().diff().dt.days

# Categorise gradient values
conditions = [
    df['Glucose_Gradient'] >= 5,
    (df['Glucose_Gradient'] > 0) & (df['Glucose_Gradient'] < 5),
    df['Glucose_Gradient'] == 0,
    df['Glucose_Gradient'] < 0
]
categories = ['Rapid Increase', 'Increase', 'No Change', 'Decrease']
df['Gradient_Category'] = np.select(conditions, categories, default='No Change')

# Checking anomalies with a threshold
threshold = 7
df['Anomaly'] = np.where(df['Glucose_Gradient'].abs() > threshold, 'Anomaly', 'Normal')

# Plotting
fig, ax1 = plt.subplots()
ax1.plot(df.index, df['Glucose_Level'], 'b-', label='Glucose Level')
ax1.set_xlabel('Date')
ax1.set_ylabel('Glucose Level', color='b')

ax2 = ax1.twinx()
ax2.plot(df.index, df['Glucose_Gradient'], 'r--', label='Glucose Gradient')
ax2.set_ylabel('Glucose Gradient', color='r')

fig.legend(loc="upper left", bbox_to_anchor=(0.1,1))
plt.title('Glucose Level and Gradient Over Time')
plt.show()

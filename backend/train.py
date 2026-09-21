import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib  # to push this model to backend, or pickle also we can use

df = pd.read_csv('../data/house_prices.csv')
df
df.head()
df.describe()
df.corr()
# how to check correlation between features and target variable

df.dtypes
(df == 0).sum()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.savefig('correlation_heatmap.png')
plt.show()

sns.pairplot(df)
plt.savefig('pairplot.png')

x = df.drop('Price_Lakhs', axis=1)
y = df['Price_Lakhs']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)

joblib.dump(model, 'model_linear.pkl')

print('Model Trained and Saved')

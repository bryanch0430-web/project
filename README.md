# Real-Time Asset Management & Predictive Analytics Platform
This platform enables users to integrate their assets, providing a comprehensive view of their total asset value and quantity. It is designed to simplify asset management by allowing users to easily track where their assets are stored. Additionally, the platform offers basic predictions on whether stocks, such as AAPL, will close higher or lower the following day and the main task is predicting cryptocurrency prices using a Bayesian LSTM model, leveraging yfinance for data, technical indicators with TA-Lib, and TensorFlow for deep learning.. These forecasts are intended solely for user reference.

### Prerequisites

What things you need to install the software and how to install them:

- Git
- FastAPI
- PostgreSQL
- Node.js
- A modern web browser

  
### Installation

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository:
    ```sh
    git clone https://github.com/bryanch0430-web/project.git
    ```
2. Install project dependencies:
    ```sh
   pip install -r requirements.txt
    ```
3. Navigate to the frontend directory:
    ```sh
    cd frontend 
    ```
4. Install project dependencies:
    ```sh
    yarn install
    ```
5. Install PostgreSQL
  
  - set the password to A7589#aaa and DataBase name = App

## Usage

How to run the project:

1. Navigate to the backend directory:
   ```sh
    cd backend 
    ```
2. Start backend
   ```sh
    uvicorn main:app 
    ```
3. Navigate to the fronted directory:
   ```sh
    cd fronend 
    ```
4. Start frontend
   ```sh
    yarn start 
    ```
How to run the crypto prediction (train and test):

1. Navigate to the backend directory:
   ```sh
    cd backend
    ```
2. Navigate to the prediction directory:
   ```sh
   cd prediction
    ```
3. Start the script
      ```sh
   python Crypto.py 
    ```

- BTC and ETH prediction perform the worst (It may need change the start date for improving the dataset)
- ENS, BNB and SOL prediction perform the best (r2 score > 0.9)
- The Bayesian LSTM is particularly suited to the task that data is noisy, and an understanding of prediction uncertainty can guide better decision-making.

## Preview
### Asset Management Page
![image](https://github.com/bryanch0430-web/project/assets/129389913/15428bf6-a278-4a0e-9a1d-74cf445cfcd0)

### Up/Down Prediction
![image](https://github.com/bryanch0430-web/project/assets/129389913/e19b66ab-a3c1-4724-8681-e9af58f0c864)

### Predicting Cryptocurrency Prices Using a Bayesian LSTM Model
![image](https://github.com/bryanch0430-web/project/assets/129389913/cc29968f-61cd-4adf-a214-88163584b500)


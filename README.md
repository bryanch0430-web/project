#Asset management & simple prediction

### Prerequisites

What things you need to install the software and how to install them:

- Git
- FastAPI
- PostgreSQL
- Node.js
- A modern web browser

- 
### Installation

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/simpleproject.git
    ```
2. Navigate to the frontend directory:
    ```sh
    cd frontend 
    ```
3. Install project dependencies:
    ```sh
    yarn install
    ```
4. Navigate to the backend directory:
      ```sh
    cd backend 
    ```

5. Install project dependencies:
    ```sh
   pip install -r requirements.txt
    ```
6. Install PostgreSQL
    ```sh
    SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:A7589#aaa@localhost:5432/App'
    ```
  set the password to A7589#aaa and DataBase name = App

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

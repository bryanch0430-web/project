import { useState } from 'react';
import Navbar from '../tools/nav_bar';
import ChartComponent from '../tools/chart_short_term';
import api from '../api';

const PredictionComponent = () => {
  const [prediction, setPrediction] = useState<String | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/predict_AAPL/');
      setPrediction(response.data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
  }; // The function to fetch the prediction of the stock trend of AAPL

  const ticker = 'AAPL'

  return (
    <div>
      <Navbar></Navbar>
      <div className="container-fluid">
        
        <div className="d-flex justify-content-center mt-2 mb-3" style={{ width: '90%', margin: 'auto' }}>
          <ChartComponent ticker={ticker} />
        </div>
        {loading && (
          <div className="d-flex justify-content-center mt-2 mb-3">
            <div>Loading prediction...</div>
          </div>
        )}
        {error && (
          <div className="d-flex justify-content-center mt-2 mb-3">
            <div>Error: {error}</div>
          </div>
        )}
        {prediction && (
          <div className="d-flex justify-content-center mt-2 mb-3">
            <div>Prediction Trend: {prediction}</div>
          </div>
        )}
        <div className="d-flex justify-content-center mt-2 mb-3">
          <button className="btn btn-outline-secondary my-3" onClick={fetchPrediction} disabled={loading}>
            Predict Trend
          </button>
        </div>
      </div>
    </div>
  );
};

export default PredictionComponent;
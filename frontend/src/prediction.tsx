import  { useEffect, useState } from 'react';
import Navbar from './nav_bar';
import api from './api';
import ChartComponent from './chart_short_term';
  
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
    };
    /*
    useEffect(() => {
      fetchPrediction();
    }, []); */
    const ticker ='AAPL'
    return (
      <div>
        <Navbar></Navbar>
        <h3 className="d-flex justify-content-center mt-3 mb-3">Short Term Closing Price Chart of {ticker}</h3>
        <ChartComponent ticker={ticker} />
        {loading && <div>Loading prediction...</div>}
        {error && <div>Error: {error}</div>}
        {prediction && (
          <div className="d-flex justify-content-center mt-3 mb-3">
            <div>Prediction Trend: {prediction}</div>
          </div>
        )}
        <div className="d-flex justify-content-center mt-3 mb-3">
            <button className="btn btn-outline-secondary my-3" onClick={fetchPrediction} disabled={loading}>
            Predict Trend
            </button>
        </div>

      </div>
    );
  };
  
  export default PredictionComponent;
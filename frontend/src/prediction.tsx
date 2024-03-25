import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {useAppDispatch} from './redux/store'
import { startPrediction } from './redux/Prediction/predictionThrunk';
import Navbar from './nav_bar';
const PredictionComponent = () => {
  const dispatch = useAppDispatch();
  const prediction = useSelector((state: any) => state.predictions.prediction);
  const predictionStatus = useSelector((state: any) => state.predictions.status);
  const predictionError = useSelector((state: any) => state.predictions.error);

  const handlePredictClick = () => {
    dispatch(startPrediction());
  };

  return (
    <div>
        <Navbar/>
      <button onClick={handlePredictClick} disabled={predictionStatus === 'loading'}>
        Predict AAPL Trend
      </button>

      {predictionStatus === 'loading' && <div>Loading prediction...</div>}

      {predictionStatus === 'failed' && <div>Error: {predictionError}</div>}

      {predictionStatus === 'succeeded' && prediction && (
        <div>
          Prediction: {prediction.trend}
        </div>
      )}
    </div>
  );
};

export default PredictionComponent;
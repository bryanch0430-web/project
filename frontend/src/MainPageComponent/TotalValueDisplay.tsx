import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { getTotalValue } from '../redux/TotalAssetWorth/totalWorthThrunks';
import { RootState } from '../redux/store';
import { useAppDispatch, useAppSelector } from '../redux/store'

const TotalValueDisplay: React.FC = () => {
  const dispatch = useAppDispatch();
  const { totalValue, loading, error } = useSelector((state: RootState) => state.totalWorth);

  useEffect(() => {
    const intervalId = setInterval(() => {
      dispatch(getTotalValue());
    }, 15000); 
    dispatch(getTotalValue());
    return () => clearInterval(intervalId);
  }, [dispatch]);

  let content;

  if (loading) {
    content = (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '200px' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  } else if (error) {
    content = (
      <div className="alert alert-danger" role="alert">
        Error: {error}
      </div>
    );
  } else {
    content = (
      <div className="card text-dark bg-light mb-3">
        <div className="card-header">Total Portfolio Value</div>
        <div className="card-body">
          <h5 className="card-title">Value</h5>
          <p className="card-text">${totalValue?.toFixed(2)} USD</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-3">
      <div className="row">
        <div className="col">
          {content}
        </div>
      </div>
    </div>
  );
};

export default TotalValueDisplay;
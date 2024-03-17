
import React, { useEffect } from 'react';
import { getTotalPrice } from '../redux/Asset/assetThunks';
import { calculateTotalValue, selectTotalValue } from '../redux/Price/assetPriceSlice';
import { useAppDispatch, useAppSelector } from '../redux/store'

const TotalValueDisplay: React.FC = () => {
  const dispatch = useAppDispatch();
  const totalValue = useAppSelector(selectTotalValue);

  useEffect(() => {
    dispatch(getTotalPrice)
  }, [dispatch]);

  return (
    <div className="container mt-3">
      <div className="card">
        <div className="card-body">
          <h5 className="card-title">Total Portfolio Value</h5>
          <p className="card-text">
            The total value of your assets is: <strong>${totalValue.toFixed(2)}</strong>
          </p>
        </div>
      </div>
    </div>
  );
};

export default TotalValueDisplay;
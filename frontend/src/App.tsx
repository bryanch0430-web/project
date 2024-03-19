import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from './redux/store';
import { fetchAssets } from './redux/Asset/assetThunks';
import { Asset } from './redux/Asset/assetSlice';
import TotalValueDisplay from './MainPage_component/TotalValueDisplay';
import App_AssetForm from './MainPage_component/App_AssetForm';
import './App.css'
import App_AssetList from './MainPage_component/App_AssetList';

const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);


  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-pantone-7453c">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">Asset Management System</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link active" aria-current="page" href="#">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">Pricing</a>
              </li>

            </ul>
          </div>
        </div>
      </nav>
      <TotalValueDisplay></TotalValueDisplay>
      <App_AssetForm></App_AssetForm>
      <App_AssetList></App_AssetList>

    </div>
  );
};

export default App;
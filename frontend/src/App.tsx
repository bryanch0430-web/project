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
      <nav className="navbar navbar-expand-lg navbar-light large-navbar bg-pantone-7453c">
        Asset Management System
      </nav>
      <TotalValueDisplay></TotalValueDisplay>
      <App_AssetForm></App_AssetForm>
      <App_AssetList></App_AssetList>
        
    </div>
  );
};

export default App;
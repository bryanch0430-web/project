import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from './redux/store';
import { fetchAssets } from './redux/Asset/assetThunks';
import { Asset } from './redux/Asset/assetSlice';
import TotalValueDisplay from './MainPage_component/TotalValueDisplay';
import App_AssetForm from './MainPage_component/App_AssetForm';
import './App.css'
import App_AssetList from './MainPage_component/App_AssetList';
import Navbar from './nav_bar';
const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);


  return (
    <div>
      <Navbar/>
      <TotalValueDisplay></TotalValueDisplay>
      <App_AssetForm></App_AssetForm>
      <App_AssetList></App_AssetList>

    </div>
  );
};

export default App;
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../redux/store';
import { fetchAssets } from '../redux/Asset/assetThunks';
import { Asset } from '../redux/Asset/assetSlice';
import TotalValueDisplay from '../MainPageComponent/TotalValueDisplay';
import App_AssetForm from '../MainPageComponent/App_AssetForm';
import './App.css'
import App_AssetList from '../MainPageComponent/App_AssetList';
import Navbar from '../tools/nav_bar';
import AssetTypeDistribution from '../MainPageComponent/Pie_Assettype';
const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);


  return (
    <div>
      <Navbar/>
      <TotalValueDisplay></TotalValueDisplay>
      <App_AssetForm></App_AssetForm>
      <App_AssetList></App_AssetList>
      <AssetTypeDistribution></AssetTypeDistribution>
    </div>
  );
};

export default App;
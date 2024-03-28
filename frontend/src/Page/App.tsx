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
import AssetLocationDistribution from '../MainPageComponent/Pie_Location';
const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);


  return (
    <div>
      <div className="col-sm-12">
      <Navbar /></div>
      <TotalValueDisplay></TotalValueDisplay>
      <App_AssetForm></App_AssetForm>
      <div className="row">
        <div className="col-sm-6">
          <App_AssetList></App_AssetList>
        </div>
        <div className="col-sm-3">
        <div className="bg-light p-2 rounded-3" style={{ width: '80%', margin: 'auto' }}>
            <AssetTypeDistribution></AssetTypeDistribution>
            <h5 className="d-flex justify-content-center align-items-center mt-3">Asset Type Distribution</h5>
          </div>
          </div>
          <div className="col-sm-3">
          <div className="bg-light p-2 rounded-3" style={{ width: '80%', margin: 'auto' }}>
            <AssetLocationDistribution></AssetLocationDistribution>
            <h5 className="d-flex justify-content-center align-items-center mt-3">Asset Location Distribution</h5>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
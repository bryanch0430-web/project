import React, { useState, useEffect } from 'react';
import './App.css'
import TotalValueDisplay from '../MainPageComponent/TotalValueDisplay'; //Total Portfolio Value
import App_AssetForm from '../MainPageComponent/App_AssetForm'; //Create New Asset  
import App_AssetList from '../MainPageComponent/App_AssetList'; //Asset List =>AssetList.tsx, UpdateQuantity.tsx & DeleteAsset.tsx  
import Navbar from '../tools/nav_bar'; // Navigation Bar  
import AssetTypeDistribution from '../MainPageComponent/Pie_Assettype';// pie chart Asset Type Distribution
import AssetLocationDistribution from '../MainPageComponent/Pie_Location'; // pie chart Asset Location Distribution 
import ChartRecordComponent from '../tools/chart_record'; // Line chart Portfolio Value over time
const App: React.FC = () => {
  return (
    <div>
    <div className="col-sm-12">
    <Navbar /></div>
    <div className="container-fluid"> 


      <div className="row">
        <div className="col-sm-6">
          <TotalValueDisplay></TotalValueDisplay>
          <App_AssetForm></App_AssetForm>
          <App_AssetList></App_AssetList>
        </div>
        <div className="col-sm-6">
          <div className="col-sm-12 mt-2 mb-2" >
            <div className="bg-light p-2 rounded-3" style={{ width: '90%', margin: 'auto' }}>
              <div style={{ width: '90%', margin: 'auto' }}>
              <ChartRecordComponent></ChartRecordComponent>
              </div>
            </div>
          </div><div className="row">
            <div className="col-sm-6 mt-3">
              <div className="bg-light p-2 rounded-3" style={{ width: '80%', margin: 'auto' }}>
                <h5 className="d-flex justify-content-center align-items-center mt-3">Asset Type Distribution</h5>
                <AssetTypeDistribution />
              </div>
            </div>
            <div className="col-sm-6 mt-3">
              <div className="bg-light p-2 rounded-3" style={{ width: '80%', margin: 'auto' }}>
                <h5 className="d-flex justify-content-center align-items-center mt-3">Asset Location Distribution</h5>
                <AssetLocationDistribution />
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>
    </div>
  );
};

export default App;
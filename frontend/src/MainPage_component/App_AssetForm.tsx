import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../redux/store';
import { fetchAssets } from '../redux/Asset/assetThunks';
import AssetForm from '../AssetComponent/createNewAsset'
import '../App.css'

const App_AssetForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);
  const [isAssetFormOpen, setIsAssetFormOpen] = useState(false);


  const openAssetForm = () => setIsAssetFormOpen(true);
  const closeAssetForm = () => setIsAssetFormOpen(false);


  useEffect(() => {
    dispatch(fetchAssets());
  }, [isAssetFormOpen]);


  return (
    <div>
       <div className="d-flex justify-content-center mt-3 mb-3">
      <button className="btn btn-outline-secondary my-3" onClick={openAssetForm}>
        Add New Asset
      </button>
      {isAssetFormOpen && (
        <AssetForm assets={assets} onClose={closeAssetForm} />
      )}

    </div>
    </div>
  );
};

export default App_AssetForm;
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../redux/store';
import { fetchAssets } from '../redux/Asset/assetThunks';
import AssetForm from '../AssetComponent/createNewAsset'
import '../Page/App.css'
import ExcelAssetForm from '../AssetComponent/ExcelImportAsset';


const App_AssetForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);
  const [isAssetFormOpen, setIsAssetFormOpen] = useState(false);
  const [isExcelAssetFormOpen, setIsExcelAssetFormOpen] = useState(false);

  const openAssetForm = () => {
    setIsAssetFormOpen(true);
    setIsExcelAssetFormOpen(false); // Ensure only one form is open at a time
  };

  const closeAssetForm = () => setIsAssetFormOpen(false);

  const openExcelAssetForm = () => {
    setIsExcelAssetFormOpen(true);
    setIsAssetFormOpen(false); // Ensure only one form is open at a time
  };

  const closeExcelAssetForm = () => setIsExcelAssetFormOpen(false);

  useEffect(() => {
    dispatch(fetchAssets());
  }, [dispatch]);

  // Function to find the next id
  const getNextId = () => {
    if (!assets.length) return 0;
    return assets.reduce((maxId, asset) => Math.max(maxId, parseInt(asset.id, 10)), 0) + 1;
  };

  return (
    <div>
      {/* Button to open the standard AssetForm */}
      <div className="d-flex justify-content-center mt-3 mb-3">
        <button className="btn btn-outline-secondary mx-2" onClick={openAssetForm}>
          Add New Asset
        </button>
        {isAssetFormOpen && (
          <AssetForm assets={assets} onClose={closeAssetForm} nextId={getNextId()} />
        )}
      </div>
      {/* Button to open the ExcelAssetForm */}
      <div className="d-flex justify-content-center mt-3 mb-3">
        <button className="btn btn-outline-secondary mx-2" onClick={openExcelAssetForm}>
          Add New Asset via Excel
        </button>
        {isExcelAssetFormOpen && (
          <ExcelAssetForm />
        )}
      </div>
      {/* Loading and Error Messages */}
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
};

export default App_AssetForm;
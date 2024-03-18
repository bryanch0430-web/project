import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from './redux/store';
import { fetchAssets } from './redux/Asset/assetThunks';
import { Asset } from './redux/Asset/assetSlice';
import AssetForm from './AssetComponent/createNewAsset'
import Quantity from './AssetComponent/updateQuantity';
import Dialog from './dialog';
import AssetsList from './AssetComponent/AssetList';
import TotalValueDisplay from './AssetComponent/TotalValueDisplay';
import './App.css'

const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);
  const [isModalOpen, setModalOpen] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);

  const [isAssetFormOpen, setIsAssetFormOpen] = useState(false);

  const openAssetForm = () => setIsAssetFormOpen(true);
  const closeAssetForm = () => setIsAssetFormOpen(false);


  useEffect(() => {
    dispatch(fetchAssets());
  }, [dispatch]);


 


  const handleEditAsset = (asset: Asset) => {
    setSelectedAsset(asset);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelectedAsset(null);
  };
  
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light large-navbar bg-pantone-7453c">
              Asset Management System 
      </nav>
      <TotalValueDisplay></TotalValueDisplay>
      <button onClick={openAssetForm}>Add New Asset</button>
      {isAssetFormOpen && (
        <AssetForm assets={assets} onClose={closeAssetForm} />
      )}
      <AssetsList assets={assets} onEdit={handleEditAsset} />
      {selectedAsset && ((
        <Dialog isOpen={isModalOpen} onClose={closeModal}>
          <Quantity
            assetId={selectedAsset.id}
            currentQuantity={selectedAsset.quantity}
            onClose={closeModal}
          />
        </Dialog> 
      ) )}


    </div>
  );
};

export default App;
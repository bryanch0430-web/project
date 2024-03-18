import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../redux/store';
import { fetchAssets } from '../redux/Asset/assetThunks';
import { Asset } from '../redux/Asset/assetSlice';
import AssetForm from '../AssetComponent/createNewAsset'
import Quantity from '../AssetComponent/updateQuantity';
import Dialog from '../dialog';
import AssetsList from '../AssetComponent/AssetList';
import DeleteAsset from '../AssetComponent/deleteAsset';
import '../App.css'


const App_AssetList: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { assets, loading, error } = useSelector((state: RootState) => state.asset);
  const [isModalOpen, setModalOpen] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [isAssetFormOpen, setIsAssetFormOpen] = useState(false);
  const [modalType, setModalType] = useState('null'); 
  const closeAssetForm = () => setIsAssetFormOpen(false);


  useEffect(() => {
    dispatch(fetchAssets());
  }, [dispatch]);


  useEffect(() => {
    dispatch(fetchAssets());
  }, [selectedAsset]);



  const handleDeleteClick = (asset: Asset) => {
    setModalType('DELETE');
    setSelectedAsset(asset);
    setModalOpen(true);
  };

  const handleEditAsset = (asset: Asset) => {
    setModalType('EDIT'); 
    setSelectedAsset(asset);
    setModalOpen(true);
  };


  const closeModal = () => {
    setModalType('null')
    setModalOpen(false);
    setSelectedAsset(null);
  };


  return (
    <div>
      {isAssetFormOpen && (
        <AssetForm assets={assets} onClose={closeAssetForm} />
      )}
      <AssetsList assets={assets} onEdit={handleEditAsset} onDelete={handleDeleteClick} />
      {selectedAsset && (
        isModalOpen && modalType === 'EDIT' ? (
          <Dialog isOpen={isModalOpen} onClose={closeModal}>
            <Quantity
              id={selectedAsset.id}
              currentQuantity={selectedAsset.quantity}
              onClose={closeModal}
            />
          </Dialog>
        ) : isModalOpen && modalType === 'DELETE' ? (
          <Dialog isOpen={isModalOpen} onClose={closeModal}>
            <DeleteAsset
              id={selectedAsset.id}
              onClose={closeModal}
            />
          </Dialog>
        ) : null
      )}

    </div>
  );
};

export default App_AssetList;
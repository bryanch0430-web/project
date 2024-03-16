import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { createAssets } from '../redux/Asset/assetThunks';
import { Asset } from '../redux/Asset/assetSlice';
import { RootState, AppDispatch } from '../redux/store';
import Dialog from '../dialog';

interface AssetFormProps {
  assets: Asset[];
  onClose: () => void;
}


const AssetForm: React.FC<AssetFormProps> = ({onClose}) => {
const dispatch = useDispatch<AppDispatch>();
  const [asset, setAsset] = useState({
    id: '',
    asset_id: '',
    asset_type: '',
    description: '',
    location: '',
    quantity: 0,
    cost_price: 0
  });

  const handleChange = (e:any) => {
    const { name, value } = e.target;
    setAsset(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e:any) => {
    e.preventDefault();
    dispatch(createAssets(asset));
  };

  const isModalOpen = true;

  return (
    <Dialog isOpen={isModalOpen} onClose={onClose}>
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="id"
        value={asset.id}
        onChange={handleChange}
        placeholder="ID"
      />
      <input
        type="text"
        name="asset_id"
        value={asset.asset_id}
        onChange={handleChange}
        placeholder="Asset ID"
      />
      <input
        type="text"
        name="asset_type"
        value={asset.asset_type}
        onChange={handleChange}
        placeholder="Asset Type"
      />
      <input
        type="text"
        name="description"
        value={asset.description}
        onChange={handleChange}
        placeholder="Description"
      />
      <input
        type="text"
        name="location"
        value={asset.location}
        onChange={handleChange}
        placeholder="Location"
      />
      <input
        type="number"
        name="quantity"
        value={asset.quantity}
        onChange={handleChange}
        placeholder="Quantity"
      />
      <input
        type="number"
        name="cost_price"
        value={asset.cost_price}
        onChange={handleChange}
        placeholder="Cost Price"
      />
      <button type="submit">Create Asset</button>
    </form>
      </Dialog>
  );
};

export default AssetForm;
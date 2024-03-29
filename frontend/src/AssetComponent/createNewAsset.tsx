import React, { useState } from 'react';
import { createAssets } from '../redux/Asset/assetThunks';
import { Asset } from '../redux/Asset/assetSlice';
import { useAppDispatch } from '../redux/store';
import Dialog from '../tools/dialog';
import { fetchAssets } from '../redux/Asset/assetThunks';
interface AssetFormProps {
  assets: Asset[];
  onClose: () => void;
  nextId: number;
}

const AssetForm: React.FC<AssetFormProps> = ({ onClose, nextId }) => {
  const dispatch = useAppDispatch();
  const isModalOpen = true;
  const [error, setError] = useState<string>('');

  // Initialize asset state with all properties except 'id'
  const [asset, setAsset] = useState<Omit<Asset, 'id'>>({
    asset_id: '',
    asset_type: '',
    location: '',
    description: '',
    quantity: 0,
    cost_price: 0,
  });

  // Handle form field changes
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setAsset(prevAsset => ({
      ...prevAsset,
      [name]: name === 'quantity' || name === 'cost_price' ? Number(value) : value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!asset.asset_id || !asset.asset_type || !asset.location) {
      setError('Please fill in all required fields.');
      return;
    }

    const newAsset: Asset = {
      ...asset,
      id: nextId.toString(),
    };

    dispatch(createAssets(newAsset));

    onClose();
    dispatch(fetchAssets());

  };

  return (
    <Dialog isOpen={isModalOpen} onClose={onClose}>
      <div className="bg-pantone-7453c">
        <nav className="navbar navbar-expand-lg navbar-light">
          <div className="container-fluid">
            <span className="navbar-brand mb-0 h1">Create Asset</span>
          </div>
        </nav>
      </div>

      <form onSubmit={handleSubmit} className="p-3">
        {error && <div className="alert alert-danger" role="alert">{error}</div>}
        <div className="mb-3">
        <input
          type="text"
          name="asset_id"
          className="form-control"
          value={asset.asset_id}
          onChange={handleChange}
          placeholder="Asset ID (required)"
          required
        />
      </div>  

      <div className="mb-3">
        <input
          type="text"
          name="asset_type"
          className="form-control"
          value={asset.asset_type}
          onChange={handleChange}
          placeholder="Asset Type (required)"
          required
        />
      </div>

      <div className="mb-3">
        <input
          type="text"
          name="description"
          className="form-control"
          value={asset.description}
          onChange={handleChange}
          placeholder="Description"
        />
      </div>

      <div className="mb-3">
        <input
          type="text"
          name="location"
          className="form-control"
          value={asset.location}
          onChange={handleChange}
          placeholder="Location (required)"
          required
        />
      </div>

      <div className="mb-3">
        <input
          type="number"
          name="quantity"
          className="form-control"
          value={asset.quantity !== 0 ? asset.quantity.toString() : ''}
          onChange={handleChange}
          placeholder="Quantity (required)"
        />
      </div>

      <div className="mb-3">
        <input
          type="number"
          name="cost_price"
          className="form-control"
          value={asset.cost_price !== 0 ? asset.cost_price.toString() : ''}
          onChange={handleChange}
          placeholder="Cost Price"
        />
      </div>


      <div className="d-flex justify-content-center">
        <button className="btn btn-primary" type="submit">Create Asset</button>
        
      </div>


    </form>
    <p className='mt-1 mb-1'>* Asset ID is the ticker in yahoo finance</p>
      <p className='mt-1 mb-1'>* Location is where the asset store in</p>
    </Dialog >
  );
};

export default AssetForm;
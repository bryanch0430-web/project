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


const AssetForm: React.FC<AssetFormProps> = ({ onClose }) => {
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

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setAsset(prevState => ({
      ...prevState,
      [name]: value
    }));
  };
  const [error, setError] = useState<string>('');
  const handleSubmit = (e: any) => {
    e.preventDefault();
    // Check for required fields
    if (!asset.id || !asset.asset_id || !asset.asset_type || !asset.location) {
      setError('Please fill in all required fields.');
      return;
    }
    dispatch(createAssets(asset));
    onClose();
  };

  const isModalOpen = true;

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
            name="id"
            className="form-control"
            value={asset.id}
            onChange={handleChange}
            placeholder="ID (required)"
            required
          />
        </div>

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
            placeholder="Quantity"
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
    </Dialog>
  );
};

export default AssetForm;
import React from 'react';
import { Asset } from '../redux/Asset/assetSlice';// Import the Asset type

interface AssetsListProps {
  assets: Asset[];
  onEdit: (asset: Asset) => void;
  onDelete: (asset: Asset) => void;
}

const AssetsList: React.FC<AssetsListProps> = ({ assets, onEdit, onDelete }) => {
  return (
    <div className="container mt-4">
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Type</th>
            <th scope="col">Location</th>
            <th scope="col">Quantity</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((asset) => (
            <tr key={asset.id}>
              <th scope="row">{asset.asset_id}</th>
              <td>{asset.asset_type}</td>
              <td>{asset.location}</td>
              <td>{asset.quantity}</td>
              <td>
                <button
                  className="btn btn-primary me-2"
                  onClick={() => onEdit(asset)}
                >
                  Update Quantity
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => onDelete(asset)}
                >
                  Delete Asset
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssetsList;
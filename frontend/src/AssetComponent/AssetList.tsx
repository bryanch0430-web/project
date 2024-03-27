import React, { useState } from 'react';
import { Asset } from '../redux/Asset/assetSlice';

interface AssetsListProps {
  assets: Asset[];
  onEdit: (asset: Asset) => void;
  onDelete: (asset: Asset) => void;
}

const AssetsList: React.FC<AssetsListProps> = ({ assets, onEdit, onDelete }) => {
  const [sortColumn, setSortColumn] = useState<string>(''); // Track the current sorting column
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc'); // Track the current sorting order

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      // If the same column is clicked again, toggle the sorting order
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      // If a different column is clicked, set it as the new sorting column and default to ascending order
      setSortColumn(column);
      setSortOrder('asc');
    }
  };

  const sortedAssets = [...assets].sort((a, b) => {
    if (sortColumn === 'asset_id') {
      return sortOrder === 'asc' ? a.asset_id.localeCompare(b.asset_id) : b.asset_id.localeCompare(a.asset_id);
    } else if (sortColumn === 'asset_type') {
      return sortOrder === 'asc' ? a.asset_type.localeCompare(b.asset_type) : b.asset_type.localeCompare(a.asset_type);
    } else if (sortColumn === 'location') {
      return sortOrder === 'asc' ? a.location.localeCompare(b.location) : b.location.localeCompare(a.location);
    } else if (sortColumn === 'quantity') {
      return sortOrder === 'asc' ? a.quantity - b.quantity : b.quantity - a.quantity;
    } else {
      // If no sorting column is selected, maintain the original order
      return 0;
    }
  });

  return (
    <div className="container mt-4">
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col" onClick={() => handleSort('asset_id')}>
              ID {sortColumn === 'asset_id' && sortOrder === 'asc' && <i className="bi bi-caret-up-fill"></i>}
              {sortColumn === 'asset_id' && sortOrder === 'desc' && <i className="bi bi-caret-down-fill"></i>}
            </th>
            <th scope="col" onClick={() => handleSort('asset_type')}>
              Type {sortColumn === 'asset_type' && sortOrder === 'asc' && <i className="bi bi-caret-up-fill"></i>}
              {sortColumn === 'asset_type' && sortOrder === 'desc' && <i className="bi bi-caret-down-fill"></i>}
            </th>
            <th scope="col" onClick={() => handleSort('location')}>
              Location {sortColumn === 'location' && sortOrder === 'asc' && <i className="bi bi-caret-up-fill"></i>}
              {sortColumn === 'location' && sortOrder === 'desc' && <i className="bi bi-caret-down-fill"></i>}
            </th>
            <th scope="col" onClick={() => handleSort('quantity')}>
              Quantity {sortColumn === 'quantity' && sortOrder === 'asc' && <i className="bi bi-caret-up-fill"></i>}
              {sortColumn === 'quantity' && sortOrder === 'desc' && <i className="bi bi-caret-down-fill"></i>}
            </th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {sortedAssets.map((asset) => (
            <tr key={asset.id}>
              <th scope="row">{asset.asset_id}</th>
              <td>{asset.asset_type}</td>
              <td>{asset.location}</td>
              <td>{asset.quantity}</td>
              <td>
                <button className="btn btn-primary me-2" onClick={() => onEdit(asset)}>
                  Update Quantity
                </button>
                <button className="btn btn-danger" onClick={() => onDelete(asset)}>
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
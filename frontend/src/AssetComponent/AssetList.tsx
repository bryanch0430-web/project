import React, { useState, useEffect } from 'react';
import api from '../api';
import { Asset } from '../redux/Asset/assetSlice';
import './AssetList.css';

interface AssetsListProps {
  assets: Asset[];
  onEdit: (asset: Asset) => void;
  onDelete: (asset: Asset) => void;
}

interface TotalValues {
  [key: string]: number | undefined;
}

const AssetsList: React.FC<AssetsListProps> = ({ assets, onEdit, onDelete }) => {
  const [expandedAssets, setExpandedAssets] = useState<{ [key: string]: boolean }>({});
  const [totalValues, setTotalValues] = useState<TotalValues>({});

  const groupedAssets = assets.reduce((acc: { [key: string]: Asset[] }, asset) => {
    const idTypeKey = `${asset.asset_id}-${asset.asset_type}`;
    if (!acc[idTypeKey]) {
      acc[idTypeKey] = [];
    }
    acc[idTypeKey].push(asset);
    return acc;
  }, {});

  const expandAll = () => {
    const allExpanded = Object.keys(groupedAssets).reduce<{ [key: string]: boolean }>((acc, key) => {
      acc[key] = true;
      return acc;
    }, {});
    setExpandedAssets(allExpanded);
  };

  const collapseAll = () => {
    setExpandedAssets({});
  };

  const toggleAssetDetails = (idTypeKey: string) => {
    setExpandedAssets(prevState => ({
      ...prevState,
      [idTypeKey]: !prevState[idTypeKey]
    }));
  };

  const fetchAllTotalValues = async () => {
    try {
      const response = await api.get('/get_total_value_by_asset/'); // Adjust the API endpoint if necessary
      const totalValuesData = response.data; // Make sure the data structure matches your actual API response
      const totalValuesMap: TotalValues = totalValuesData.reduce((acc: TotalValues, currentValue: { asset_id: string; total_value: number }) => {
        acc[currentValue.asset_id] = currentValue.total_value;
        return acc;
      }, {});
      setTotalValues(totalValuesMap);
    } catch (error) {
      console.error('Error fetching total values:', error);
      // Handle errors as appropriate for your application
    }
  };

  useEffect(() => {
    fetchAllTotalValues();
  
    const intervalId = setInterval(() => {
      fetchAllTotalValues();
    }, 10000);
  
    return () => clearInterval(intervalId);
  }, []); 

  return (
    <div>
      <link rel="stylesheet" href="/AssetList.css" />
      <div className="bg-light p-2 rounded-3">
        <div className="container mt-3">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5>Asset List</h5>
            <div>
              <button className="btn btn-outline-primary btn-sm me-2" onClick={expandAll}>
                Show All
              </button>
              <button className="btn btn-outline-secondary btn-sm" onClick={collapseAll}>
                Close All
              </button>
            </div>
          </div>
          {Object.entries(groupedAssets).map(([idTypeKey, groupedAssetList]) => (
            <div key={idTypeKey} className="card custom-asset-card mb-3">
              <div className="card-header_" onClick={() => toggleAssetDetails(idTypeKey)}>
                <div className="card-title">
                  <div className="d-flex justify-content-between">
                    <div className="d-flex align-items-center">
                      <span className="mx-2">{groupedAssetList[0].asset_id}</span>
                      <span>{groupedAssetList[0].asset_type}</span>
                    </div>

                    <div className="d-flex align-items-center justify-content-end">
                      <span className="mx-2">
                        {totalValues[groupedAssetList[0].asset_id] !== undefined
                          ? `$${totalValues[groupedAssetList[0].asset_id]!.toFixed(2)}`
                          : 'Loading...'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {expandedAssets[idTypeKey] && (
                <div className="card-body">
                  {groupedAssetList.map((asset, index) => (
                    <div key={asset.id} className={`asset-item ${index > 0 ? 'mt-3' : ''}`}>
                      <div className="asset-info">
                        <p className="card-text">Location: {asset.location}</p>
                        <p className="card-text">Quantity: {asset.quantity}</p>
                      </div>
                      <div className="asset-actions">
                        <button onClick={() => onEdit(asset)} className="btn btn-primary btn-sm me-2">
                          Edit
                        </button>
                        <button onClick={() => onDelete(asset)} className="btn btn-danger btn-sm">
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AssetsList;
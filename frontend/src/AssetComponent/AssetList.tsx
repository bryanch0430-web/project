import React, { useState } from 'react';
import { useEffect } from 'react';
import { Asset } from '../redux/Asset/assetSlice';
import './AssetList.css';
import api from '../api';

interface AssetsListProps {
  assets: Asset[];
  onEdit: (asset: Asset) => void;
  onDelete: (asset: Asset) => void;
}

const AssetsList: React.FC<AssetsListProps> = ({ assets, onEdit, onDelete }) => {
  const [expandedAssets, setExpandedAssets] = useState<{ [key: string]: boolean }>({});
  const [totalValue, setTotalValue] = useState(null);

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



  const fetchTotalValue = async (asset_id: string) => {
    try {
      const totalValueResponse = await api.get(`/get_total_value_by_asset/${asset_id}/`);
      return totalValueResponse.data.totalValue;
    } catch (error) {
      // Handle the error
    }
  };

  useEffect(() => {
    const fetchTotalValue = async () => {
      try {
        const totalValueResponse = await api.get(`/get_total_value_by_asset/`);
        setTotalValue(totalValueResponse.data);
        console.log(totalValueResponse.data);
      } catch (error) {
        // Handle the error
      }
    };
    fetchTotalValue();
  }, []);


  return (
<div>
      <link rel="stylesheet" href="/AssetList.css" />
      <div className="container mt-3">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5> Asset List</h5>
          <div>
            <button className="btn btn-outline-primary btn-sm me-2" onClick={expandAll}>Show All</button>
            <button className="btn btn-outline-secondary btn-sm" onClick={collapseAll}>Close All</button>
          </div>
        </div>
        {Object.entries(groupedAssets).map(([idTypeKey, groupedAssetList]) => (


          <div key={idTypeKey} className="card custom-asset-card mb-3">
            <div className="card-header_" onClick={() => toggleAssetDetails(idTypeKey)}>
              <div className="card-title">
                <span className="d-inline-block mx-2">{groupedAssetList[0].asset_id}</span>

                <span className="d-inline-block">{groupedAssetList[0].asset_type}</span>
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
                      <button className="btn btn-primary btn-sm" onClick={(e) => { e.stopPropagation(); onEdit(asset); }}>Edit</button>
                      <button className="btn btn-danger btn-sm" onClick={(e) => { e.stopPropagation(); onDelete(asset); }}>Delete</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AssetsList;
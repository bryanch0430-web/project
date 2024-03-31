import React, { useState, useEffect } from 'react';
import api from '../api';
import { Asset } from '../redux/Asset/assetSlice';
import './AssetList.css';
import { fetchAssets } from '../redux/Asset/assetThunks';

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
      const response = await api.get('/get_total_value_by_asset/');
      const totalValuesData = response.data;
      const totalValuesMap: TotalValues = totalValuesData.reduce((acc: TotalValues, currentValue: { asset_id: string; total_value: number }) => {
        acc[currentValue.asset_id] = currentValue.total_value;
        return acc;
      }, {});
      setTotalValues(totalValuesMap);
      fetchAssets();
    } catch (error) {
      console.error('Error fetching total values:', error);
    }
  };

  useEffect(() => {
    fetchAllTotalValues();
  
    const intervalId = setInterval(() => {
      fetchAllTotalValues();
    }, 10000);
  
    return () => clearInterval(intervalId);

  }, []);


  const sortAssetsByTotalValue = (a: [string, Asset[]], b: [string, Asset[]]): number => {
    const totalValueA = (totalValues[a[1][0]?.asset_id] ?? 0) /a[1].length;
    const totalValueB = (totalValues[b[1][0]?.asset_id] ?? 0) /b[1].length;
  
    return totalValueB - totalValueA;
  };

  const orderedGroupedAssets = Object.entries(groupedAssets).sort(sortAssetsByTotalValue);
  console.log('Sorted Assets:', orderedGroupedAssets);

  return (
    <div>
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
          {orderedGroupedAssets.map(([idTypeKey, groupedAssetList]) => (
            <div key={idTypeKey} className="custom-asset-card mb-3">
              <div className="card-header_" onClick={() => toggleAssetDetails(idTypeKey)}>
                <div className="card-title">
                  <div className="d-flex justify-content-between">
                    <div className="d-flex align-items-center">
                      <b className="mx-2">{groupedAssetList[0].asset_id}</b>
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
              {/*  The following code block is a ternary operator that checks if that asset is expanded or not. And the table is show the Asset's Location with its Quantity*/}
              {expandedAssets[idTypeKey] && (
                <div className="card-body">
                  <span className="mx-2">{groupedAssetList[0].asset_type}</span>
                  <table className="table mt-2">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Location</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {groupedAssetList.map((asset, index) => (
                        <tr key={asset.asset_id + "-" + index}>
                          <th scope="row">{index + 1}</th>
                          <td>{asset.location}</td>
                          <td>
                          {asset.quantity}
                          </td>
                          <td>
                            <button
                              className="btn btn-primary btn-sm mx-1"
                              onClick={() => onEdit(asset)}
                            >
                              Edit
                            </button>
                            <button
                              className="btn btn-danger btn-sm mx-1"
                              onClick={() => onDelete(asset)}
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
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
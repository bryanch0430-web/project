import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PieChart from '../tools/pie';
import { AssetDistribution } from '../tools/pie';
import api from '../api';

const AssetTypeDistribution: React.FC = () => {
  const [assetDistribution, setAssetDistribution] = useState<AssetDistribution>({});
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    

    const fetchAssetDistribution = async () => {
      setIsLoading(true);
      try {
        const response = await api.get('/asset_distribution_by_type/');
        setAssetDistribution(response.data.asset_distribution);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('An unknown error occurred');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchAssetDistribution();

    const intervalId = setInterval(fetchAssetDistribution, 100000); 

    return () => clearInterval(intervalId);
  }, []);


  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error} and please input the correct asset</p>;
  if (!assetDistribution) return <p>No Data</p>

  return (
    <div>
      <PieChart assetDistribution={assetDistribution} />
    </div>
  );
};

export default AssetTypeDistribution;
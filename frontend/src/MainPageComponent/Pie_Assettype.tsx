import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PieChart from '../tools/pie';
import { AssetDistribution } from '../tools/pie';

const AssetTypeDistribution: React.FC = () => {
  const [assetDistribution, setAssetDistribution] = useState<AssetDistribution>({});
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAssetDistribution = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get('/api/asset-distribution');
        setAssetDistribution(response.data.asset_distribution);
      } catch (err) {
        if (err instanceof Error) {
            setError(err.message);
         } 
      } finally {
        setIsLoading(false);
      }
    };

    fetchAssetDistribution();
  }, []);

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Asset Types Distribution</h2>
      <PieChart assetDistribution={assetDistribution} />
    </div>
  );
};

export default AssetTypeDistribution;
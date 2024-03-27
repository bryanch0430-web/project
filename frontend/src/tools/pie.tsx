import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';


ChartJS.register(ArcElement, Tooltip, Legend);

export interface AssetDistribution {
    [asset: string]: number;
  }
  
interface PieChartProps {
  assetDistribution: AssetDistribution;
}

const PieChart: React.FC<PieChartProps> = ({ assetDistribution }) => {
  const data = {
    labels: Object.keys(assetDistribution),
    datasets: [
      {
        data: Object.values(assetDistribution),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#C9CB3F',
          '#FF9F40',
        ],
        hoverBackgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#C9CB3F',
          '#FF9F40',
        ],
      },
    ],
  };

  return <Pie data={data} />;
};

export default PieChart;
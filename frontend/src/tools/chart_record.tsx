import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import api from '../api';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';


interface PortfolioEntry {
    timestamp: string;
    total_value: number;
  }

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );
  
const ChartRecordComponent: React.FC = () => {  const [portfolioData, setPortfolioData] = useState<{
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      fill: boolean;
      backgroundColor: string;
      borderColor: string;
    }[];
  }>({
    labels: [],
    datasets: [
      {
        label: 'Portfolio Value',
        data: [],
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  });

  useEffect(() => {
    // Fetch portfolio values from the FastAPI backend using Axios
    const fetchData = async () => {
      try {
        const response = await api.get<PortfolioEntry[]>('/historical_values/');
        const data = response.data;

        // Process data for the chart
        const labels = data.map((entry: PortfolioEntry) => entry.timestamp);
        const values = data.map((entry: PortfolioEntry) => entry.total_value);

        setPortfolioData(prevData => ({
          ...prevData,
          labels: labels,
          datasets: [
            {
              ...prevData.datasets[0],
              data: values,
            },
          ],
        }));
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h5 className="d-flex justify-content-center align-items-center mt-3">Portfolio Values Over Time</h5>
      <Line data={portfolioData} />
    </div>
  );
}

export default ChartRecordComponent;
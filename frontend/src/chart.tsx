import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

// Make sure the API import path matches your project's file structure
// This import must also be at the top of the file.
import api from './api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface ChartComponentProps {
  ticker: string;
}

interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    fill: boolean;
    borderColor: string;
    tension: number;
  }>;
}

type Record = {
  Open: number;
  High: number;
  Low: number;
  Close: number;
  Volume: number;
  Dividends: number;
  Stock_Splits: number;
};

type DataResponse = {
  data: {
    [key: string]: Record;
  };
};

const ChartComponent: React.FC<ChartComponentProps> = ({ ticker }) => {
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchTickerData = async () => {
      setLoading(true);
      try {
        const response = await api.get<DataResponse>(`/ticker_data/${ticker}`);
        setChartData(formatChartData(response.data));
      } catch (error) {
        setError('Failed to fetch chart data');
      } finally {
        setLoading(false);
      }
    };

    fetchTickerData();
  }, [ticker]);

  const formatChartData = (dataResponse: DataResponse): ChartData => {
    const dates = Object.keys(dataResponse.data).sort();
    const closePrices = dates.map(date => dataResponse.data[date].Close);

    const chartData: ChartData = {
      labels: dates,
      datasets: [
        {
          label: 'Close Price',
          data: closePrices,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };

    return chartData;
  };

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        chartData && <Line data={chartData} options={{ responsive: true }} />
      )}
    </div>
  );
};

export default ChartComponent;  
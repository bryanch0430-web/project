import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import api from './api';


interface ChartComponentProps {
  ticker: string;
}

// Define the structure for the chart data
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

// Define the expected structure of the stock data response
interface DataResponse {
  [date: string]: {
    close: number;
    // ...other properties if available
  };
}

const ChartComponent: React.FC<ChartComponentProps> = ({ ticker }) => {
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchTickerData = async () => {
      setLoading(true);
      try {
        const response = await api.get<DataResponse>(`/ticker_data/${ticker}`);
        console.log((response.data));
        setChartData(formatChartData(response.data));
      } catch (err) {
        const error = err as Error;
        if (axios.isAxiosError(error)) {
          setError(error.message);
        } else {
          setError('Error fetching data');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTickerData();
  }, [ticker]);

  const formatChartData = (data: DataResponse): ChartData => {
    return {
      labels: Object.keys(data).map((date) => new Date(date).toLocaleDateString()),
      datasets: [
        {
          label: `Price of ${ticker}`,
          data: Object.values(data).map((val) => val.close),
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };
  };
  
  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}

    </div>
  );
};
//      {chartData && (
//  <Line data={chartData} />
//  )}
export default ChartComponent;
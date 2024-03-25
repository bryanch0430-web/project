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

  const formatChartData = (dataResponse: DataResponse) => {
    // Extract dates and sort them to ensure the chart follows the chronological order
    const dates = Object.keys(dataResponse.data).sort();
  
    // Map the sorted dates to their respective 'Close' values
    const closePrices = dates.map(date => {
      const record = dataResponse.data[date];
      // TypeScript knows that `record` is of type StockRecord or undefined
      return record ? record.Close : null;
    }).filter((price): price is number => price !== null); // Type guard to remove nulls
  
    // Create the dataset for the Line component
    const chartData = {
      labels: dates,
      datasets: [
        {
          label: 'Close Price',
          data: closePrices,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }
      ]
    };
  
    return chartData;
  };

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {chartData && (
        <Line data={chartData} />
      )}
    </div>
  );
};

export default ChartComponent;
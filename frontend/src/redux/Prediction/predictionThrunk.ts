import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';
import api from '../../api'; 

export const startPrediction = createAsyncThunk(
  'predictions/startPrediction',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/predict_AAPL/')
      return response.data;
    } catch (err) {
        let error: AxiosError = err as AxiosError; 
        if (!error.response) {
          throw err;
        }
        return rejectWithValue(error.response.data);
      }
  }
);
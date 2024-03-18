import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../api';
import { AxiosError } from 'axios';

export const getTotalValue = createAsyncThunk(
    'portfolio/getTotalValue',
    async (_, { rejectWithValue }) => {
      try {
        const response = await api.get('/get_total_value/'); // Assuming GET request
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
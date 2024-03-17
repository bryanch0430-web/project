import { createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../api'; 
import { AxiosError } from 'axios';


export const getAllPrices = createAsyncThunk(
    'assets/getAllPrices',
    async (_, { rejectWithValue }) => {
      try {
        const response = await api.get('/get_current_prices/');
        console.log(response)
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
  
  //all_total_quantity
  
  export const getAllTotalQuantity = createAsyncThunk(
    'assets/getAllTotalQuantity',
    async (_, { rejectWithValue }) => {
      try {
        const response = await api.get('/all_total_quantity/');
        console.log(response)
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
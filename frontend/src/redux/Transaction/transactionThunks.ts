import { createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../api'; 
import { AxiosError } from 'axios';
import {Transaction} from './transactionSlice'

export const fetchTransaction = createAsyncThunk(
  'asset/fetchTransaction',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/transaction/'); 

      console.log(response.data);
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

export const createTransaction = createAsyncThunk(
  'asset/createTransaction',
  async (transaction: Transaction, { rejectWithValue }) => {
    try {
      const response = await api.post('/transaction/', transaction);
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

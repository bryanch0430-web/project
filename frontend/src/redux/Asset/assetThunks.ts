import { createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../api'; 
import { AxiosError } from 'axios';
import {Asset} from './assetSlice'

export const fetchAssets = createAsyncThunk(
  'asset/fetchAssets',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/assets/'); 
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

export const createAssets = createAsyncThunk(
  'asset/createAssets',
  async (asset: Asset, { rejectWithValue }) => {
    try {
      const response = await api.post('/assets/', asset);
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


export const updateAsset = createAsyncThunk(
  'asset/updateAsset',
  async ({ id, quantity }: { id: string; quantity: number }, { rejectWithValue }) => {
    try {
      const response = await api.patch(`/assets/${id}/`, { quantity });
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


export const getAllPrices = createAsyncThunk(
  'assets/getAllPrices',
  async (tickers, { rejectWithValue }) => {
    try {
      const response = await api.get('/get_current_prices/', { params: { tickers } });
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
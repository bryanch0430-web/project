import { createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../api'; 
import { AxiosError } from 'axios';
import {Asset} from './assetSlice'

export const fetchAssets = createAsyncThunk(
  'asset/fetchAssets',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/assets/'); 
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



export const getTotalPrice = createAsyncThunk(
  'asset/totalValue',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.patch(`/get_total_value/`, _);
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


export const deleteAsset = createAsyncThunk(
  'assets/deleteAsset',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await api.delete(`/assets/${id}`);
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

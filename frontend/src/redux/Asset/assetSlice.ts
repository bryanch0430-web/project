import { createSlice,PayloadAction } from "@reduxjs/toolkit";
import { fetchAssets, updateAsset, deleteAsset } from './assetThunks';

export interface Asset {
    id: string;
    asset_id: string;
    asset_type: string;
    location: string;
    description: string;  
    quantity: number;
    cost_price: number;
  }

interface AssetState {
    assets: Asset[];
    loading: boolean;
    error: string | null;
  }
  
const initialState: AssetState = {
    assets: [],
    loading: false,
    error: null,
  };

const assetSlice = createSlice({
    name: 'asset',
    initialState,
    reducers: {
        
    },
    extraReducers: (builder) => {
        builder
          .addCase(fetchAssets.pending, (state) => {
            state.loading = true;
            state.error = null;
          })
          .addCase(fetchAssets.fulfilled, (state, action) => {
            state.loading = false;
            state.assets = action.payload;
          })
          .addCase(fetchAssets.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
          })
          .addCase(updateAsset.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
          })
          .addCase(deleteAsset.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
          })
          ;
    },
  });

export default assetSlice.reducer;
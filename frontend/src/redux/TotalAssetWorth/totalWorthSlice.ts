import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getTotalValue } from './totalWorthThrunks';

interface TotalWorthState {
  totalValue: number | null;
  loading: boolean;
  error: string | null;
}

const initialState: TotalWorthState = {
  totalValue: null,
  loading: false,
  error: null,
};


const totalWorthSlice = createSlice({
  name: 'totalWorth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getTotalValue.pending, (state) => {
        state.loading = true;
      })
      .addCase(getTotalValue.fulfilled, (state, action) => {
        state.totalValue = action.payload;
        state.loading = false;
      })
      .addCase(getTotalValue.rejected, (state, action) => {
        state.error = action.payload as string;
        state.loading = false;
      });
  },
});

export default totalWorthSlice.reducer;
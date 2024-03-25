import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {startPrediction} from './predictionThrunk'

export interface Prediction {
    date: Date
    trend: string
  }
  
interface PredictionState {
    prediction: Prediction[];
    loading: boolean;
    error: string | null;
  }
  
const initialState: PredictionState = {
    prediction: [],
    loading: false,
    error: null,
  };

const predictionsSlice = createSlice({
  name: 'predictions',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(startPrediction.pending, (state) => {
      state.loading = true;
      state.error = null;
    })
    .addCase(startPrediction.fulfilled, (state, action) => {
      state.loading = false;
      state.prediction = action.payload;
    })
    .addCase(startPrediction.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
  },
});

export default predictionsSlice.reducer;
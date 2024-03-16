import { createSlice } from '@reduxjs/toolkit';
import { RootState } from '../store';
import { getAllPrices, getAllTotalQuantity} from './assetPriceThrunk'

interface AssetDataState {
  prices: { [key: string]: number };
  quantities: { [key: string]: number };
  totalValue: number;
}

const initialState: AssetDataState = {
  prices: {},
  quantities: {},
  totalValue: 0,
};

export const assetPriceSlice = createSlice({
  name: 'assetPrice',
  initialState,
  reducers: {
    calculateTotalValue(state) {
      state.totalValue = Object.keys(state.quantities).reduce((acc, assetId) => {
        const quantity = state.quantities[assetId];
        const price = state.prices[assetId];
        return acc + (quantity * price || 0);
      }, 0);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getAllPrices.fulfilled, (state, action) => {
        action.payload.forEach((priceInfo: { ticker: string; current_price: number }) => {
          state.prices[priceInfo.ticker] = priceInfo.current_price;
        });
      })
      .addCase(getAllTotalQuantity.fulfilled, (state, action) => {
        state.quantities = action.payload;
      });
  },
});

export const { calculateTotalValue } = assetPriceSlice.actions;

export const selectTotalValue = (state: RootState) => state.assetPrice.totalValue;

export default assetPriceSlice.reducer;
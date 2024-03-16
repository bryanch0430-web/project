import { createSlice,PayloadAction } from "@reduxjs/toolkit";
import { fetchTransaction } from './transactionThunks';

export interface Transaction {
    transaction_id: string
    asset_index_id: string
    quantity: number
    buying_date: Date
    buying_price: number
  }
  
interface TransactionState {
    transaction: Transaction[];
    loading: boolean;
    error: string | null;
  }
  
const initialState: TransactionState = {
    transaction: [],
    loading: false,
    error: null,
  };

const transactionSlice = createSlice({
    name: 'transaction',
    initialState,
    reducers: {
        
    },
    extraReducers: (builder) => {
        builder
          .addCase(fetchTransaction.pending, (state) => {
            state.loading = true;
            state.error = null;
          })
          .addCase(fetchTransaction.fulfilled, (state, action) => {
            state.loading = false;
            state.transaction = action.payload;
          })
          .addCase(fetchTransaction.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
          });
        
      },
  });

export default transactionSlice.reducer;
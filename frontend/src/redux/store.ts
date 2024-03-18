import { configureStore } from "@reduxjs/toolkit";
import assetReducer from "./Asset/assetSlice";
import transactionReducer from "./Transaction/transactionSlice";
import totalWorthReducer from "./TotalAssetWorth/totalWorthSlice";
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

export const store = configureStore({

    reducer: {
        asset:assetReducer,
        transaction: transactionReducer,
        totalWorth: totalWorthReducer
    },
});
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
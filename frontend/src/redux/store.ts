import { configureStore } from "@reduxjs/toolkit";
import assetReducer from "./Asset/assetSlice";
import transactionReducer from "./Transaction/transactionSlice";
import assetPriceReducer from "./Price/assetPriceSlice";
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

export const store = configureStore({

    reducer: {
        asset:assetReducer,
        transaction: transactionReducer,
        assetPrice: assetPriceReducer
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
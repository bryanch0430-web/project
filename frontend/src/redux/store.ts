import { configureStore } from "@reduxjs/toolkit";
import assetReducer from "./Asset/assetSlice";
import transactionReducer from "./Transaction/transactionSlice";

export const store = configureStore({

    reducer: {
        asset:assetReducer,
        transaction: transactionReducer
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
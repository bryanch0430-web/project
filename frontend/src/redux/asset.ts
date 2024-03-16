import { configureStore } from "@reduxjs/toolkit";
import assetReducer from "./Asset/assetSlice";

export const store = configureStore({

    reducer: {
        asset:assetReducer
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
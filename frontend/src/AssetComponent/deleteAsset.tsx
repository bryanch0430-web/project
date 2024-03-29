import React, { useState, FC } from 'react';
import { useDispatch } from 'react-redux';
import { deleteAsset, fetchAssets } from '../redux/Asset/assetThunks';
import Dialog from '../tools/dialog';
import { useAppDispatch, useAppSelector } from '../redux/store'

interface AssetFormProps {
  id: string;
  onClose: () => void;
}
const DeleteAsset: FC<AssetFormProps> = ({ id, onClose }) => {
  const dispatch = useAppDispatch();

  const handleDelete = () => {
    dispatch(deleteAsset(id));
    onClose();
    dispatch(fetchAssets());//refresh the asset list
    
  };

  const handleCancel = () => {
    onClose();
  }

  return (
    <Dialog isOpen={true} onClose={onClose}>
      <div className="bg-pantone-7453c">
        <nav className="navbar navbar-expand-lg navbar-light">
          <div className="container-fluid">
            <span className="navbar-brand mb-0 h1">Confirm Deletion</span>
          </div>
        </nav>
      </div>
      <div className="p-3 text-center">
        <h5 className="mb-4">Do you really want to delete this asset?</h5>
        <div className="d-flex justify-content-center">
          <button className="btn btn-danger me-2" onClick={handleDelete}>Yes, Delete</button>
          <button className="btn btn-secondary" onClick={handleCancel}>No, Cancel</button>
        </div>
      </div>
    </Dialog>
  );
};

export default DeleteAsset;
import React, { useState, FC } from 'react';
import { useDispatch } from 'react-redux';
import { updateAsset } from '../redux/Asset/assetThunks';
import Dialog from '../tools/dialog';
import { useAppDispatch, useAppSelector } from '../redux/store'

interface AssetFormProps {
  id: string;
  currentQuantity: number;
  onClose: () => void;
}

const Quantity: FC<AssetFormProps> = ({ id, currentQuantity, onClose }) => {
  const [quantity, setQuantity] = useState(currentQuantity.toString());
  const dispatch = useAppDispatch();

  const isModalOpen = true; // Replace with actual logic to control modal visibility

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const quantityNum = parseFloat(quantity);
    if (!isNaN(quantityNum) && quantityNum >= 0) {
      dispatch(updateAsset({ id: id, quantity: quantityNum }));
      onClose(); // Close the modal after dispatch
    } else {
      alert("Please enter a valid quantity");
    }
  };

  return (
    <Dialog isOpen={isModalOpen} onClose={onClose}>
      <div className="bg-pantone-7453c">
        <nav className="navbar navbar-expand-lg navbar-light">
          <div className="container-fluid">
            <span className="navbar-brand mb-0 h1">Update Asset Quantity</span>
          </div>
        </nav>
      </div>
      <form onSubmit={handleSubmit} className="p-4">
        <div className="mb-3">
          <label htmlFor="quantity" className="form-label">Quantity:</label>
          <input
            type="number"
            className="form-control"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            min="0"
            step="any" // Allows for floating point numbers
          />
        </div>

        <div className="d-flex justify-content-center">
          <button className="btn btn-primary mb-3" type="submit">Submit</button>
        </div>
      </form>
    </Dialog>
  );
};

export default Quantity;
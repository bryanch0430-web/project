import React, { useState, FC } from 'react';
import { useDispatch } from 'react-redux';
import { updateAsset } from '../redux/Asset/assetThunks';
import Dialog from '../dialog';
import { useAppDispatch, useAppSelector } from '../redux/store'

interface AssetFormProps {
  assetId: string;
  currentQuantity: number;
  onClose: () => void;
}

const Quantity: FC<AssetFormProps> = ({ assetId, currentQuantity, onClose }) => {
  const [quantity, setQuantity] = useState(currentQuantity.toString());
  const dispatch = useAppDispatch();

  const isModalOpen = true; // Replace with actual logic to control modal visibility

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const quantityNum = parseFloat(quantity);
    if (!isNaN(quantityNum) && quantityNum >= 0) {
      dispatch(updateAsset({ id: assetId, quantity: quantityNum }));
      onClose(); // Close the modal after dispatch
    } else {
      alert("Please enter a valid quantity");
    }
  };

  return (
    <Dialog isOpen={isModalOpen} onClose={onClose}>
      <h2>Update Asset Quantity</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="quantity">Quantity:</label>
        <input
          type="number"
          id="quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          min="0"
          step="any" // Allows for floating point numbers
        />
        <button type="submit">Submit</button>
      </form>
    </Dialog>
  );
};

export default Quantity;
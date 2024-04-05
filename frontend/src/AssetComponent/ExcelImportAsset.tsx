import React, { useState } from 'react';
import api from '../api';
import { useAppDispatch } from '../redux/store';
import Dialog from '../tools/dialog';

const ExcelAssetForm: React.FC = () => {
  const dispatch = useAppDispatch();
  const isModalOpen = true;
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadError, setUploadError] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setFile(files[0]);
    }
  };

  const handleFileUpload = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setUploadError('Please select a file to upload.');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/excel_to_db/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      // Handle response here
      console.log(response.data);
      setUploading(false);
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadError('Error uploading file');
      setUploading(false);
    }
  };

  return (
    <Dialog isOpen={isModalOpen} onClose={() => { /* handle close */ }}>
      {/* ... existing form fields and handlers ... */}
      
      {/* File upload form */}
      <form onSubmit={handleFileUpload} className="p-3">
        {uploadError && (
          <div className="alert alert-danger" role="alert">
            {uploadError}
          </div>
        )}
        <div className="mb-3">
          <input
            type="file"
            name="file"
            className="form-control"
            onChange={handleFileChange}
            required
          />
        </div>
        <div className="d-flex justify-content-center">
          <button className="btn btn-success" type="submit" disabled={uploading}>
            {uploading ? 'Uploading...' : 'Upload Excel File'}
          </button>
        </div>
      </form>
    </Dialog>
  );
};

export default ExcelAssetForm;
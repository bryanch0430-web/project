import React, { useState } from 'react';
import api from '../api';
import { useAppDispatch } from '../redux/store';
import Dialog from '../tools/dialog';

const ExcelAssetForm: React.FC<{ closeForm: () => void }> = ({ closeForm }) => {
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

            console.log(response.data);
            closeForm();
            setUploading(false);
        } catch (error) {
            console.error('Error uploading file:', error);
            setUploadError('Error uploading file');
            setUploading(false);
        }
    };


    return (
        <Dialog isOpen={isModalOpen} onClose={closeForm}>
            <div className="bg-pantone-7453c">
                <nav className="navbar navbar-expand-lg navbar-light">
                    <div className="container-fluid">
                        <span className="navbar-brand mb-0 h1">Create Asset via Excel</span>
                    </div>
                </nav>
            </div>

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
                <p  className="mt-2">Download this excel template from git:
                

                <a
                    href="https://github.com/bryanch0430-web/project/blob/cdd20394d59be9b61db05a57618b723e145309ab/Book1.xlsx"
                    download="Book1.xlsx"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Template
                </a>
                </p>
            </form>
        </Dialog>
    );
};

export default ExcelAssetForm;
import React from 'react';
import { CSSProperties } from 'react';

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const Dialog: React.FC<DialogProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.dialog}>
        <button style={styles.closeButton} onClick={onClose}>
          &times;
        </button>
        {children}
      </div>
    </div>
  );
};

const styles: { [key: string]: CSSProperties } = {
  overlay: {
    position: 'fixed', 
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  dialog: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '5px',
    minWidth: '300px',
    zIndex: 1000,
  },
  closeButton: {
    float: 'right' as const, 
    border: 'none',
    background: 'transparent',
    fontSize: '1.5rem',
    cursor: 'pointer',
  },
};

export default Dialog;

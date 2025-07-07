import React from 'react';
import microphone from '../assets/microphone.png';

const Recorder = () => {
  return (
    <button>
        <img src={microphone} alt="recorder" />
    </button>
  );
};

export default Recorder;
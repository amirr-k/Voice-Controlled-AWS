import React from 'react';
import microphone from '../assets/a7f5a253d2b3ff0e994ecbac333f8a406bf598d27f812e18e69070fc1d4ddf4e.jpg';
import './recorder.css';
const Recorder = () => {
  return (
    <button className="recorder">
      <img src={microphone} alt="microphone" className="microphone" />
    </button>
  );
};

export default Recorder;
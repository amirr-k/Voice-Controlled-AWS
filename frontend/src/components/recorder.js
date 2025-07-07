import React from 'react';
import microphone from '../assets/a7f5a253d2b3ff0e994ecbac333f8a406bf598d27f812e18e69070fc1d4ddf4e.jpg';
import './recorder.css';
const Recorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  function startRecording() = async () => {
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    mediaRecorder.onstop = () => {
      setIsRecording(false);
  }
  function stopRecording() {
    setIsRecording(false);
  }
  return (
    <button className="recorder">
      {isRecording ? (
      <img src={microphone} alt="microphone" className="microphone" />
    </button>
  );
};

export default Recorder;
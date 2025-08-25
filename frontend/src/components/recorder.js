import React, { useState, useRef } from 'react';
import microphone from '../assets/a7f5a253d2b3ff0e994ecbac333f8a406bf598d27f812e18e69070fc1d4ddf4e.jpg';
import './recorder.css';

const Recorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  const getSupportedMimeType = () => {
    return 'audio/mp4';   // force Safari MP4
  };

  const startRecording = async () => {
    try {
      setIsRecording(true);
      
      // Get user input
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });
      
      streamRef.current = stream;
      
      // Create MediaRecorder for recording audio
      const mimeType = getSupportedMimeType();
      const mediaRecorder = mimeType 
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream);
      
      mediaRecorderRef.current = mediaRecorder;
      
      // Collect audio data for the recording
      const audioChunks = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: mimeType || 'audio/mp4' });
        setAudioBlob(audioBlob);
        setIsRecording(false);
        
        // Stop all tracks to turn off microphone
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
        }
        
        console.log('Recording stopped, blob created:', audioBlob);
        // Still need to create the backend to upload the audio blob
        // TO DO
        uploadAudio(audioBlob, 'mp4');
      };
      
      mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        setIsRecording(false);
      };
      
      // Start recording
      mediaRecorder.start(1000); // Collect data every 1 second
      
    } catch (error) {
      console.error('Error starting recording:', error);
      setIsRecording(false);
      
      if (error.name === 'NotAllowedError') {
        alert('Microphone access denied. Please allow microphone access and try again.');
      } else if (error.name === 'NotFoundError') {
        alert('No microphone found. Please connect a microphone and try again.');
      } else {
        alert('Error accessing microphone: ' + error.message);
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  };

  const uploadAudio = async (audioBlob, fileExt) => {
    setIsProcessing(true);
    
    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('audio', audioBlob, `recording.${fileExt}`);
      
      const API_ENDPOINT = 'https://odcbdy9auh.execute-api.us-east-1.amazonaws.com/test/upload-audio';
      
      console.log('Uploading audio blob of size:', audioBlob.size);
      
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Upload successful:', result);
        // Handle successful upload
      } else {
        throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
      }
      
    } catch (error) {
      console.error('Upload error:', error);
      // TO DO: Handle upload error -- still need to create the backend
      console.log('Backend not functioning - audio blob created successfully');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleButtonClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="recorder-container">
      <button 
        className={`recorder ${isRecording ? 'recording' : ''} ${isProcessing ? 'processing' : ''}`}
        onClick={handleButtonClick}
        disabled={isProcessing}
      >
        <img 
          src={microphone} 
          alt="microphone" 
          className="microphone" 
        />
      </button>
      
      <div className="status-text">
        {isProcessing && <p>Processing audio...</p>}
        {isRecording && <p>Recording... Click to stop</p>}
        {!isRecording && !isProcessing && <p>Click to start recording</p>}
        {audioBlob && !isProcessing && (
          <p>Recording ready ({Math.round(audioBlob.size / 1024)}KB)</p>
        )}
      </div>
        
    </div>
  );
};

export default Recorder;
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders voice recorder app', () => {
  render(<App />);
  
  // Check if the microphone button is rendered
  const microphoneButton = screen.getByRole('button');
  expect(microphoneButton).toBeInTheDocument();
  
  // Check if the microphone image is present
  const microphoneImage = screen.getByAltText('microphone');
  expect(microphoneImage).toBeInTheDocument();
  
  // Check if the status text is displayed
  const statusText = screen.getByText('Click to start recording');
  expect(statusText).toBeInTheDocument();
});

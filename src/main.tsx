import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Hide loading screen when app is rendered
const hideLoadingScreen = () => {
  const loadingScreen = document.getElementById('loading-screen');
  if (loadingScreen) {
    loadingScreen.classList.add('hidden');
    // Remove the loading screen from DOM after animation
    setTimeout(() => {
      loadingScreen.remove();
    }, 500);
  }
};

const root = createRoot(document.getElementById("root")!);
root.render(<App />);

// Hide loading screen after the app is rendered
window.addEventListener('load', hideLoadingScreen);

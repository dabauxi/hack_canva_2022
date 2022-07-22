import './App.css';
import React from 'react';
import Heading from './Components';
import Webcam from './Webcam';
import UploadForm from './Upload';
import Images from './ImagePolling';


class App extends React.Component {
  render() {
    return (
      <div>
          <UploadForm></UploadForm>
      </div>
    )

  }
}

export default App;

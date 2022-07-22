import React from 'react';


class Webcam extends React.Component {
    render() {
      return (
        <img src="http://127.0.0.1:5000/video_feed" />
      );
    }
  }


export default Webcam;

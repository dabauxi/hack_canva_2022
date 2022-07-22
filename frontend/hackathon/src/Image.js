import React from 'react';


class Image extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
      return (
        <img src={`data:image/jpeg;base64,${self.props.data}`} />
      );
    }
  }


export default Image;

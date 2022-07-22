

import React from 'react';
import axios from 'axios';
import { Button, CircularProgress } from '@mui/material';
import { Container } from '@mui/system';


class UploadForm extends React.Component {


    constructor(props) {
        super(props);
        this.state = {
            selectedFiles: null,
            original: null,
            modified: null,
            fileupload: false
        };


    }

    handleChange(event) {
    this.setState({ title: event.target.value });
    }
    handleSubmit(event) {
    console.log("handle submit called")
    console.log(event)
    event.preventDefault();
    }


    onFileChange = event => {

    // Update the state
    this.setState({ selectedFiles: event.target.files });
    
    };

    onFileUpload = () => {
    this.setState({fileUpload: true})
    const formData = new FormData();

    let uploadImages = [];

    for (let i = 0; i < this.state.selectedFiles.length; i++) {
        uploadImages.push(this.state.selectedFiles[i]);
    }
    // Details of the uploaded file
    console.log(uploadImages);
    for (let i = 0 ; i < uploadImages.length ; i++) {
        formData.append("uploaded-images", uploadImages[i]);
    }
    // formData.append("upload-images", uploadImages)
    // Request made to the backend api
    // Send formData object
    let response = axios.post("http://api:5000/upload", formData).then(response => this.setState({original: response.data.original, modified: response.data.modified, fileUpload: false})).catch(error => console.log("error happened in post calls"))
    console.log(response)
    };

    render() {
      let images = <div></div>
      if (this.state.original != null) {
        const zip = (a, b) => a.map((k, i) => [k, b[i]]);
        const result = zip(this.state.original, this.state.modified)
        images =  <p>
        <div>{result.map((elem, index) => {
            return <div> <img src={`data:image/jpeg;base64,${this.state.original[index]}`} /><img src={`data:image/jpeg;base64,${this.state.modified[index]}`} /></div>
          })}</div>

        </p>
      }
      
      let fileupload = <div></div>
      if (this.state.fileUpload === true) {
          fileupload = <div><CircularProgress /></div>
      }

      return (
        <Container fixed>
                  <h1>Canva Hackathon 2022</h1>

        <div>

        {/* <a href='http://127.0.0.1:5000/reset'><button>Reset</button></a> */}
        <form onSubmit={this.handleSubmit}>
        <Button variant="outlined" component="label">
          Choose Files
        <input
          hidden
          type="file"
          multiple name="file"
          onChange={this.onFileChange}
        />
        </Button>
             <Button variant="contained" onClick={this.onFileUpload}>
                  Upload!
                </Button>
                {fileupload}

        </form>
        {images}
        </div>
        </Container>
      );
    }
  }


export default UploadForm;

import logo from './logo.png';
import './App.css';
import React, {Component} from 'react';
import HomeIcon from '@mui/icons-material/Home';

class App extends Component {

  /**
   * constructor function
   * @param {Object} props 
   * @memberof App
   */
  constructor(props) {
    super(props);
    this.state = {
      display: true,
    }
    this.displayContent = this.displayContent.bind(this);
  }

  displayContent() {

  }


  /**
   * Render function
   * @return {*}
   * @memberof App
   */
  render() {
    //  F8B195   F67280   C06C84   6C5B7B   355C7D 
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="logo" alt="logo" />
          <span className="title">House Guard</span>
          <HomeIcon className="buttons"/>
        </header>
      </div>
    );
  }

}

export default App;

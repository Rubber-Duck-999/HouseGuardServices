import logo from './logo.png';
import './App.css';
import React, {Component} from 'react';
import Box from '@mui/material/Box';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import RestoreIcon from '@mui/icons-material/Restore';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ArchiveIcon from '@mui/icons-material/Archive';
import ImageIcon from '@mui/icons-material/Image';
import Paper from '@mui/material/Paper';

import View from './pages/View';

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
      value: 1,
    }
    this.displayContent = this.displayContent.bind(this);
  }

  /**
   * displayContent function
   * @param {Int} value 
   * @memberof App
   */
   displayContent(value) {
    this.setState({
      value: value,
    });
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
        </header>
        <Box>
          <View
            viewValue={this.state.value}
          >
          </View>
          <Paper className="App-Bar" sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={24}>
            <BottomNavigation
              showLabels
              value={this.state.value}
              onChange={(event, value) => this.displayContent(value)}
            >
              <BottomNavigationAction label="Weather" icon={<RestoreIcon />} />
              <BottomNavigationAction label="Alarm" icon={<FavoriteIcon />} />
              <BottomNavigationAction label="Images" icon={<ImageIcon />} />
              <BottomNavigationAction label="Download" icon={<ArchiveIcon />} />
            </BottomNavigation>
          </Paper>
        </Box>
      </div>
    );
  }

}

export default App;

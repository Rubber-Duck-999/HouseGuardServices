import React, {Component} from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import PropTypes from 'prop-types';

class View extends Component {

  /**
   * constructor function
   * @param {Object} props 
   * @memberof View
   */
  constructor(props) {
    super(props);
    this.state = {
      messages: [],
      viewValue: 0,
    };
  }

  componentDidMount() {
    this.getData();
  }

  componentDidUpdate() {
    if (this.props.viewValue !== this.state.viewValue) {
      this.getData();
      this.setState({
        viewValue: this.props.viewValue,
      });
    }
  }

  /**
   * getData function
   * @memberof View
   */
  getData() {
    const list_messages = [
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 40`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      },
      {
        time: 'Yesterday',
        value: 'Temperature: 30`C'
      }
    ];
    this.setState({
      messages: list_messages,
    });
  }


  /**
   * Render function
   * @return {*}
   * @memberof View
   */
  render() {
    //  F8B195   F67280   C06C84   6C5B7B   355C7D
    console.log(this.state);
    return (
      <div className="DataView">
        <List>
          {this.state.messages.map(({ time, value }, index) => (
          <ListItem button key={index}>
            <ListItemText primary={time} secondary={value} />
          </ListItem>
          ))}
        </List>
      </div>
    );
  }
}

View.propTypes = {
  viewValue: PropTypes.number.isRequired,
};

export default View;

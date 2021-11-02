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
      days: 1,
      viewValue: 0,
      average_temperature: 0.0,
    };
  }

  componentDidMount() {
    this.callTemperature();
  }

  componentDidUpdate() {
    if (this.props.viewValue !== this.state.viewValue) {
      this.callTemperature();
      this.setState({
        viewValue: this.props.viewValue,
      });
    }
  }

  /**
   * callTemperature function
   * @memberof View
   */
  async callTemperature() {
    try {
      const response = await fetch(`http://192.168.0.21:5000/temp/hours/` + this.state.days);
      const json = await response.json();
      console.log(json);
      this.setState({
        messages: json.Records,
        average_temperature: json.AverageTemperature,
      });
    } catch (error) {
      console.log(error);
    }
  }


  /**
   * Render function
   * @return {*}
   * @memberof View
   */
  render() {
    //  F8B195   F67280   C06C84   6C5B7B   355C7D
    return (
      <div className="DataView">
        {this.state.show_messages && 
        <List>
          {this.state.messages.map(({ TimeOfTemperature, Temperature }, index) => (
          <ListItem button key={index}>
            <ListItemText primary={TimeOfTemperature} secondary={Temperature} />
          </ListItem>
          ))}
        </List>}
        {this.state.average_temperature}
      </div>
    );
  }
}

View.propTypes = {
  viewValue: PropTypes.number.isRequired,
};

export default View;

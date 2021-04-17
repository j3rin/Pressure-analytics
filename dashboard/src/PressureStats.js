import React, { Component } from 'react';
import { Chart } from "react-google-charts"; 
class PressureStats extends Component {
   
    render() {
        // //getting data from json
        // let theData = this.props.data
        return <div>  <center>     
          <p> <b>Number of Contractions</b> {this.props.num_contractions}</p>
          <p><b>Contraction per Second</b> {this.props.contraction_per_sec}</p></center>
        </div>;
    }
  }
  export default PressureStats;
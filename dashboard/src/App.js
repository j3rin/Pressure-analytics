import pressure from './pressure.json';
import PressureChart from './PressureChart.js'
import PressureStats from './PressureStats.js'
function App() {
  return (
      <div className="App">
        {<div><PressureChart data={pressure.pressure_points}/>
          <PressureStats
                 num_contractions={pressure.count_contractions}
                 contraction_per_sec={pressure.contractions_per_sec}
                 /></div>}
 
      </div>
  );
}

export default App;

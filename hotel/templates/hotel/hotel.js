import React from 'react';

const sampleJSON = {
  "string": "PluralSight",
  "number": 1
};

function App() {
  return(
    <div>
      <p>String : {sampleJSON.string}</p>
      <p>Number : {sampleJSON.number}</p>
    </div>
  )
}

ReactDOM.render(<App />, document.getElementById('app'));
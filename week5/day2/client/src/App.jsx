import { useState, useEffect, useRef } from 'react';

function App() {
  const [elements, setElements] = useState([]);
  const ref = useRef();

  const handleAdd = (val) => {
    if (val) {
      setElements([...elements, val]);
      ref.current.value = '';  
    }
  };

  useEffect(() => {
    fetch("http://localhost:5000/api/elements")  
      .then(res => res.json())
      .then(res => setElements(res));
  }, []);

  return (
    <div className="app-container">
      <div className="input-section">
        <input
          type="text"
          ref={ref}
          placeholder="Enter text"
        />
        <button onClick={() => handleAdd(ref.current.value)}>Add</button>
      </div>

      <hr />
      
      <h1>Previously Added Elements</h1>
      
      <section className="elements-list">
        {elements.map((e, index) => (
          <div key={index} className="element-item">
            <h3>{e}</h3>
          </div>
        ))}
      </section>
    </div>
  );
}

export default App;

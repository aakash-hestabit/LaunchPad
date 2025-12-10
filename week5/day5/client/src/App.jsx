import { useState, useEffect, useRef } from "react";
import axios from "axios";

function App() {
  const [elements, setElements] = useState([]);
  const ref = useRef();

  const handleAdd = async (val) => {
    if (val) {
      try {
        await axios.post("https://my.domain/api/elements", {
          content: val,
        });
        setElements((prev) => [...prev, val]);
        ref.current.value = "";
      } catch (error) {
        console.error("Error sending element:", error);
      }
    }
  };

  useEffect(() => {
    axios
      .get("https://my.domain/api/elements")
      .then((res) => {
        const ele = res.data.map((r) => r.content);
        setElements(ele);
      })
      .catch((err) => console.error("Fetch error:", err));
  }, []);

  return (
    <div className="app-container">
      <div className="input-section">
        <input type="text" ref={ref} placeholder="Enter text" />
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

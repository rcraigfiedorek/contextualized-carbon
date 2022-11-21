import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import logo from "./logo.svg";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <CompanyEmissionInfo />
      </header>
    </div>
  );
}

export default App;

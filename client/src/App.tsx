import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import { NavBar } from "./components/NavBar";

function App() {
  return (
    <div className="App">
      <NavBar />

      <div className="App-body">
        <CompanyEmissionInfo />
      </div>

      <div className="search-menu-toggle">Search</div>
    </div>
  );
}

export default App;

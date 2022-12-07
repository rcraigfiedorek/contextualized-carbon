import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import { NavBar } from "./components/NavBar";
import { Sidebar } from "./components/Sidebar";

function App() {
  return (
    <div className="App">
      <NavBar />
      <div className="App-body">
        <Sidebar />

        <CompanyEmissionInfo />
      </div>
    </div>
  );
}

export default App;

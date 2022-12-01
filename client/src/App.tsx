import "bootstrap/dist/css/bootstrap.min.css";
import _ from "lodash";
import { useEffect, useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import Spinner from "react-bootstrap/Spinner";
import { CompanyOutput } from "./api";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import { api } from "./config";
import epa from "./epa.svg";
import github from "./github.svg";
import logo from "./logo.svg";

function App() {
  const [initCompany, setInitCompany] = useState<CompanyOutput>();

  useEffect(() => {
    api
      .apiCompaniesGet(1, 40, undefined, 2021, "fully_owned_emissions", 2021)
      .then(({ data: { companies } }) => setInitCompany(_.sample(companies)));
  }, []);

  return (
    <div className="App">
      <div className="App-header">
        <img src={logo} className="logo" />
        <span className="header-text">
          Corporations pollute, not individuals.
        </span>
        <Dropdown className="hamburger-dropdown">
          <Dropdown.Toggle>Menu</Dropdown.Toggle>
          <Dropdown.Menu>
            <Dropdown.Item href="https://github.com/rcraigfiedorek/emissions-bot">
              Source code
              <img src={github} className="hamburger-dropdown-icon" />
            </Dropdown.Item>
            <Dropdown.Item href="https://enviro.epa.gov/envirofacts/ghg/">
              Source data
              <img src={epa} className="hamburger-dropdown-icon" />
            </Dropdown.Item>
            <Dropdown.Item href="https://craigf.io">
              About the author
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <div className="App-body">
        {!!initCompany ? (
          <CompanyEmissionInfo initialCompany={initCompany} />
        ) : (
          <Spinner animation="border" role="status" />
        )}
      </div>
    </div>
  );
}

export default App;

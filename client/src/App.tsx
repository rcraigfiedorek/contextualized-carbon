import "bootstrap/dist/css/bootstrap.min.css";
import _ from "lodash";
import { useEffect, useState } from "react";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
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
      <Navbar expand={false} fixed="top" className="emissions-navbar">
        <Navbar.Brand>
          <img src={logo} className="logo" />
          <span className="header-text">
            Corporations pollute, not individuals.
          </span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-collapse" />
        <Navbar.Collapse id="navbar-collapse">
          <Nav>
            <div className="nav-link-container">
              <Nav.Link
                href="https://github.com/rcraigfiedorek/emissions-bot"
                target="_blank"
                rel="noopener noreferrer"
                active={false}
              >
                Source code
                <img src={github} className="nav-link-icon" />
              </Nav.Link>
            </div>
            <div className="nav-link-container">
              <Nav.Link
                href="https://enviro.epa.gov/envirofacts/ghg"
                target="_blank"
                rel="noopener noreferrer"
                active={false}
              >
                Source data
                <img src={epa} className="nav-link-icon" />
              </Nav.Link>
            </div>
            <div className="nav-link-container">
              <Nav.Link
                href="https://craigf.io"
                target="_blank"
                rel="noopener noreferrer"
                active={false}
              >
                About the author
              </Nav.Link>
            </div>
          </Nav>
        </Navbar.Collapse>
      </Navbar>

      <div className="App-body">
        {!!initCompany ? (
          <CompanyEmissionInfo initialCompany={initCompany} />
        ) : (
          <Spinner
            className="initializing-spinner"
            animation="border"
            role="status"
          />
        )}
      </div>
    </div>
  );
}

export default App;

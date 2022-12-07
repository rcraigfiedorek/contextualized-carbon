import "bootstrap/dist/css/bootstrap.min.css";
import _ from "lodash";
import { useEffect, useState } from "react";
import { CompanyOutput } from "./api";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import { NavBar } from "./components/NavBar";
import { api } from "./config";

function App() {
  const [initCompany, setInitCompany] = useState<CompanyOutput>();

  useEffect(() => {
    api
      .apiCompaniesGet(1, 40, undefined, 2021, "fully_owned_emissions", 2021)
      .then(({ data: { companies } }) => setInitCompany(_.sample(companies)));
  }, []);

  return (
    <div className="App">
      <NavBar />

      <div className="App-body">
        <CompanyEmissionInfo />
      </div>
    </div>
  );
}

export default App;

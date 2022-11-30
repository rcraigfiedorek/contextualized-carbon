import _ from "lodash";
import { useEffect, useState } from "react";
import Spinner from "react-bootstrap/Spinner";
import { CompanyOutput } from "./api";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
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

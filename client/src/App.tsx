import _ from "lodash";
import { useEffect, useState } from "react";
import Spinner from "react-bootstrap/Spinner";
import { CompanyOutput, DefaultApi } from "./api";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import logo from "./logo.svg";

function App() {
  const [initCompany, setInitCompany] = useState<CompanyOutput | null>(null);

  useEffect(() => {
    const api = new DefaultApi();
    api
      .apiCompaniesGet(1, 1)
      .then(({ data: { total } }) =>
        api.apiCompaniesCompanyIdGet(_.random(1, total || 1))
      )
      .then(({ data }) => setInitCompany(data));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {(initCompany && (
          <CompanyEmissionInfo initialCompany={initCompany} />
        )) || <Spinner animation="border" />}
      </header>
    </div>
  );
}

export default App;

import "bootstrap/dist/css/bootstrap.min.css";
import _ from "lodash";
import { useEffect, useState } from "react";
import { CompanyOutput } from "./api";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import { NavBar } from "./components/NavBar";
import { Sidebar } from "./components/Sidebar";
import { useWorstOffender } from "./hooks/useWorstOffender";

function App() {
  const availableYears = _.map(_.range(2010, 2022), _.toString);
  const initialYear = "2021";

  const [displayedCompany, setDisplayedCompany] = useState<CompanyOutput>();
  const [displayedYear, setDisplayedYear] = useState<string>();

  const getRandomWorstOffender = useWorstOffender(availableYears);

  const displayRandomWorstOffender = (year?: string) => {
    setDisplayedCompany(undefined);
    setDisplayedYear(undefined);
    getRandomWorstOffender(year).then(
      ([worstOffenderCompany, worstOffenderYear]) => {
        setDisplayedCompany(worstOffenderCompany);
        setDisplayedYear(worstOffenderYear);
      }
    );
  };

  useEffect(() => {
    displayRandomWorstOffender(initialYear);
  }, []);

  return (
    <div className="App">
      <NavBar />
      <div className="App-body">
        <Sidebar
          company={displayedCompany}
          year={displayedYear}
          setCompany={setDisplayedCompany}
          setYear={setDisplayedYear}
        />

        <CompanyEmissionInfo
          company={displayedCompany}
          year={displayedYear}
          onCompanyClick={displayRandomWorstOffender}
        />
      </div>
    </div>
  );
}

export default App;

import "bootstrap/dist/css/bootstrap.min.css";
import _ from "lodash";
import { useEffect, useState } from "react";
import { CompanyOutput } from "./api";
import "./App.css";
import { CompanyEmissionInfo } from "./components/CompanyEmissionInfo";
import { NavBar } from "./components/NavBar";
import { Sidebar } from "./components/Sidebar";
import { useWorstOffender } from "./hooks/useWorstOffender";

const AVAILABLE_YEARS = _.map(_.range(2010, 2022), _.toString);
const INITIAL_YEAR = "2021";

function App() {
  const [displayedCompany, setDisplayedCompany] = useState<CompanyOutput>();
  const [displayedYear, setDisplayedYear] = useState<string>();
  const [navbarExpanded, setNavbarExpanded] = useState<boolean>(false);

  const getRandomWorstOffender = useWorstOffender(AVAILABLE_YEARS);

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
    displayRandomWorstOffender(INITIAL_YEAR);
  }, []);

  return (
    <div className="App">
      <NavBar expanded={navbarExpanded} setExpanded={setNavbarExpanded} />
      <div className="App-body" onClick={() => setNavbarExpanded(false)}>
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

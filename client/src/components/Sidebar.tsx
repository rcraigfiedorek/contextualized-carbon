import classNames from "classnames";
import _ from "lodash";
import { useMemo, useState } from "react";
import { CloseButton, Form } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import { CompanyOutput } from "../api";
import { CompanyDropdown } from "./CompanyDropdown";

interface SidebarProps {
  company?: CompanyOutput;
  setCompany: (company?: CompanyOutput) => void;
  year?: string;
  setYear: (year?: string) => void;
}

export const Sidebar: React.FunctionComponent<SidebarProps> = ({
  company,
  year,
  setCompany,
  setYear,
}) => {
  const [showSidebar, setShowSidebar] = useState<boolean>(false);

  const yearOptions = useMemo(
    () =>
      _.chain(company?.emissions_by_year)
        .keys()
        .map((yearOption) => <option value={yearOption}>{yearOption}</option>)
        .value(),
    [company]
  );

  return (
    <div className={classNames("sidebar-container", { visible: showSidebar })}>
      <div className="sidebar">
        <div className="sidebar-header">
          Search
          <CloseButton onClick={() => setShowSidebar(false)} />
        </div>
        <Form className="sidebar-form">
          <Form.Group className="sidebar-form-group">
            <Form.Label>Year</Form.Label>
            <Form.Select
              className="year-select inline-block"
              value={year}
              onChange={(event) => setYear(event.target.value)}
            >
              {yearOptions}
            </Form.Select>
          </Form.Group>
          <Form.Group className="sidebar-form-group">
            <Form.Label>Company</Form.Label>
            <CompanyDropdown
              yearFilter={year}
              selectedCompany={company}
              setSelectedCompany={setCompany}
            />
          </Form.Group>
        </Form>

        <div className="sidebar-footer">
          <p>
            Note: the emissions included here are reported only from large GHG
            emission sources and fuel and industrial gas suppliers. Most
            organizations' indirect emissions are not included.{" "}
            <a
              href="https://www.epa.gov/climateleadership/scope-1-and-scope-2-inventory-guidance"
              target="_blank"
              rel="noopener noreferrer"
            >
              Read more about different types of emissions.
            </a>
          </p>
          <p>
            <a
              href="https://github.com/rcraigfiedorek/emissions-bot/blob/main/SOURCES.md"
              target="_blank"
              rel="noopener noreferrer"
            >
              Click here to see sources on emission comparisons.
            </a>
          </p>
        </div>

        <Button
          className="search-menu-toggle"
          onClick={() => setShowSidebar(!showSidebar)}
          bsPrefix="no-css"
        >
          Search
        </Button>
      </div>
    </div>
  );
};

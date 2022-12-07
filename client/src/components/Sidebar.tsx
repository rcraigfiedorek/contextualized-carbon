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
  // return (
  //   <Offcanvas show={show} onHide={() => setShow(false)}>
  //     <Offcanvas.Header closeButton>
  //       <Offcanvas.Title>Offcanvas</Offcanvas.Title>
  //     </Offcanvas.Header>
  //     <Offcanvas.Body>
  //       Some text as placeholder. In real life you can have the elements you
  //       have chosen. Like, text, images, lists, etc.
  //     </Offcanvas.Body>
  //   </Offcanvas>
  // );
};

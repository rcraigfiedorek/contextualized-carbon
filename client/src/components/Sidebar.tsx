import classNames from "classnames";
import { useState } from "react";
import { CloseButton, Form } from "react-bootstrap";
import Button from "react-bootstrap/Button";

interface SidebarProps {}

export const Sidebar: React.FunctionComponent<SidebarProps> = () => {
  const [showSidebar, setShowSidebar] = useState<boolean>(false);

  return (
    <div className={classNames("sidebar-container", { visible: showSidebar })}>
      <div className="sidebar">
        <div className="sidebar-header">
          Search
          <CloseButton onClick={() => setShowSidebar(false)} />
        </div>
        <Form>
          <Form.Group>
            <Form.Label>Year</Form.Label>
            <Form.Select
              className="year-select inline-block"
              // value={selectedYear}
              // onChange={(event) => setSelectedYear(event.target.value)}
            >
              {[]}
            </Form.Select>
          </Form.Group>
          <Form.Group>
            <Form.Label>Company</Form.Label>
            {/* <CompanyDropdown /> */}
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

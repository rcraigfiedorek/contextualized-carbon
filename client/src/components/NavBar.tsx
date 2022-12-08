import _ from "lodash";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import c2es from "../c2es.png";
import epa from "../epa.svg";
import github from "../github.svg";
import logo from "../logo.svg";
import openapi from "../openapi.svg";

interface NavBarProps {}

export const NavBar: React.FunctionComponent<NavBarProps> = ({}) => {
  const navBarLinks: NavBarLinkProps[] = [
    { href: "/api/docs", label: "API Documentation", iconSrc: openapi },
    {
      href: "https://github.com/rcraigfiedorek/emissions-bot",
      label: "Source code",
      iconSrc: github,
    },
    {
      href: "https://www.epa.gov/ghgreporting",
      label: "Source data",
      iconSrc: epa,
    },
    {
      href: "https://www.c2es.org/content/carbon-tax-basics/",
      label: "Climate solutions",
      iconSrc: c2es,
    },
    { href: "https://craigf.io", label: "About the author" },
  ];

  return (
    <Navbar expand={false} fixed="top" className="emissions-navbar">
      <Navbar.Brand>
        <img src={logo} className="logo" />
        <span className="header-text">
          Corporations pollute, not individuals.
        </span>
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="navbar-collapse" />
      <Navbar.Collapse id="navbar-collapse">
        <Nav>{_.map(navBarLinks, NavBarLink)}</Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

interface NavBarLinkProps {
  href: string;
  label: string;
  iconSrc?: string;
}

const NavBarLink: React.FunctionComponent<NavBarLinkProps> = ({
  href,
  label,
  iconSrc,
}) => {
  return (
    <div className="nav-link-container">
      <Nav.Link
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        active={false}
      >
        {label}
      </Nav.Link>
      {iconSrc ? <img src={iconSrc} className="nav-link-icon" /> : null}
    </div>
  );
};

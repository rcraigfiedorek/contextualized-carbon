import _ from "lodash";
import React, { useEffect, useState } from "react";
import Select from "react-select";
import { CompanyOutput, DefaultApi } from "../api";
import { CompanyDropdown } from "./CompanyDropdown";

interface CompanyEmissionInfoProps {}

export const CompanyEmissionInfo: React.FunctionComponent<
  CompanyEmissionInfoProps
> = ({}) => {
  const [companyOutput, setCompanyOutput] = useState<CompanyOutput | null>(
    null
  );
  const [year, setYear] = useState<string | null>(null);
  const [emission, setEmission] = useState<number | null>(null);

  useEffect(() => {
    new DefaultApi().apiCompaniesGet().then(({ data: { companies } }) => {
      const newCompany = _.head(companies);
      if (newCompany) {
        setCompanyOutput(newCompany);
        setYear(_.chain(newCompany.emissions_by_year).keys().max().value());
      }
    });
  }, []);

  useEffect(() => {
    setEmission(
      companyOutput && year
        ? _.get(companyOutput.emissions_by_year, year, null)
        : null
    );
  }, [companyOutput, year]);

  const yearOptions = _.chain(companyOutput?.emissions_by_year)
    .keys()
    .map((yearOption) => ({
      value: yearOption,
      label: yearOption,
    }))
    .value();

  if (!companyOutput || !year || !emission) {
    return <></>;
  } else
    return (
      <span>
        <span>{"In "}</span>
        <span>
          <Select options={yearOptions} />
        </span>
        <span>{", facilities in the US owned by "}</span>
        <span>
          <CompanyDropdown />
        </span>
        <span>
          {` reported emissions equivalent to at least ${emission} tonnes of CO`}
          <sub>{"2"}</sub>
          {"."}
        </span>
      </span>
    );
};

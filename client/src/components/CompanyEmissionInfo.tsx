import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import Form from "react-bootstrap/Form";
import { CompanyOutput, DefaultApi } from "../api";
import { CompanyDropdown } from "./CompanyDropdown";

interface CompanyEmissionInfoProps {
  initialCompany: CompanyOutput;
}

export const CompanyEmissionInfo: React.FunctionComponent<
  CompanyEmissionInfoProps
> = ({ initialCompany }) => {
  const [selectedCompany, setSelectedCompany] =
    useState<CompanyOutput>(initialCompany);
  const [selectedYear, setSelectedYear] = useState<string>(
    _.chain(selectedCompany.emissions_by_year).keys().max().value()
  );

  const [currentFact, setCurrentFact] = useState<string>();
  const [factShuffleKey, setFactShuffleKey] = useState<number>();
  const [factIsLoading, setFactIsLoading] = useState<boolean>(true);

  const emission = useMemo(
    () =>
      _.get(selectedCompany, [
        "emissions_by_year",
        selectedYear,
        "fully_owned_emissions",
      ]),
    [selectedCompany, selectedYear]
  );

  const yearOptions = useMemo(
    () =>
      _.chain(selectedCompany?.emissions_by_year)
        .keys()
        .map((yearOption) => <option value={yearOption}>{yearOption}</option>)
        .value(),
    [selectedCompany]
  );

  useEffect(() => {
    setFactIsLoading(true);
    new DefaultApi()
      .apiEmissionComparisonFactGet(emission, factShuffleKey)
      .then(({ data: { fact, next_shuffle_key } }) => {
        setFactShuffleKey(next_shuffle_key);
        setCurrentFact(fact);
        setFactIsLoading(false);
      });
  }, [emission]);

  if (!selectedCompany || !selectedYear || !emission) {
    return <></>;
  } else
    return (
      <>
        <div>
          <span>{"In "}</span>
          <span>
            <Form.Select
              value={selectedYear}
              onChange={(event) => setSelectedYear(event.target.value)}
            >
              {yearOptions}
            </Form.Select>
          </span>
          <span>{", facilities in the US owned by "}</span>
          <span>
            <CompanyDropdown
              yearFilter={selectedYear}
              setSelectedCompany={setSelectedCompany}
              selectedCompany={selectedCompany}
              typeaheadClassNames="inline-block"
            />
          </span>
          <span>
            {` reported emissions equivalent to at least ${emission} tonnes of CO`}
            <sub>{"2"}</sub>
            {"."}
          </span>
        </div>
        <div>{!factIsLoading ? <>{currentFact}</> : <></>}</div>
      </>
    );
};

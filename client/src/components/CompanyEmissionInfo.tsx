import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Spinner from "react-bootstrap/Spinner";
import { CompanyOutput } from "../api";
import { api } from "../config";
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
  const [currentFactShuffleKey, setCurrentFactShuffleKey] = useState<number>();
  const [nextFactShuffleKey, setNextFactShuffleKey] = useState<number>();
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

  function refreshFact(increment = true) {
    setFactIsLoading(true);
    api
      .apiEmissionComparisonFactGet(emission, nextFactShuffleKey)
      .then(({ data: { fact, current_shuffle_key, next_shuffle_key } }) => {
        setCurrentFact(fact);
        if (increment || nextFactShuffleKey === undefined) {
          setCurrentFactShuffleKey(current_shuffle_key);
          setNextFactShuffleKey(next_shuffle_key);
        }
        setFactIsLoading(false);
      });
  }

  useEffect(() => {
    refreshFact(false);
  }, [emission]);

  if (!selectedCompany || !selectedYear || !emission) {
    return <></>;
  } else
    return (
      <>
        <div className="text-card">
          <span>{"In "}</span>
          <Form.Select
            className="year-select inline-block"
            value={selectedYear}
            onChange={(event) => setSelectedYear(event.target.value)}
          >
            {yearOptions}
          </Form.Select>
          <span>{", facilities in the US owned by "}</span>
          <CompanyDropdown
            yearFilter={selectedYear}
            setSelectedCompany={setSelectedCompany}
            selectedCompany={selectedCompany}
            typeaheadClassNames="inline-block"
          />
          <span>
            {` reported emissions equivalent to at least ${emission} tonnes of CO`}
            <sub>{"2"}</sub>
            {"."}
          </span>
        </div>
        <Button
          className="text-card"
          disabled={factIsLoading}
          onClick={!factIsLoading ? () => refreshFact() : undefined}
          bsPrefix="no-css"
        >
          {!factIsLoading ? (
            <>{currentFact}</>
          ) : (
            <Spinner
              className="initializing-spinner"
              animation="border"
              role="status"
            />
          )}
        </Button>
      </>
    );
};

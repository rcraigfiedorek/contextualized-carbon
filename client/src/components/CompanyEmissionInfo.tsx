import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import Select from "react-select";
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

  const [currentFact, setCurrentFact] = useState<string | undefined>();
  const [factShuffleKey, setFactShuffleKey] = useState<number | undefined>();
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

  const yearOptions = _.chain(selectedCompany?.emissions_by_year)
    .keys()
    .map((yearOption) => ({
      value: yearOption,
      label: yearOption,
    }))
    .value();

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
            <Select
              options={yearOptions}
              onChange={(singleValue) =>
                singleValue && setSelectedYear(singleValue.value)
              }
            />
          </span>
          <span>{", facilities in the US owned by "}</span>
          <span>
            <CompanyDropdown
              yearFilter={selectedYear}
              setSelectedCompany={setSelectedCompany}
              selectedCompany={selectedCompany}
            />
          </span>
          <span>
            {` reported emissions equivalent to at least ${emission} tonnes of CO`}
            <sub>{"2"}</sub>
            {"."}
          </span>
        </div>
        <div>
          (factIsLoading ? <>{currentFact}</> : <></>)
        </div>
      </>
    );
};

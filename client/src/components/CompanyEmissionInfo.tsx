import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Spinner from "react-bootstrap/Spinner";
import Tooltip from "react-bootstrap/Tooltip";
import { CompanyOutput } from "../api";
import { api } from "../config";
import { CompanyDropdown } from "./CompanyDropdown";

interface CompanyEmissionInfoProps {}

export const CompanyEmissionInfo: React.FunctionComponent<
  CompanyEmissionInfoProps
> = () => {
  const availableYears = _.map(_.range(2010, 2022), _.toString);
  const initialYear = "2021";

  const [selectedCompany, setSelectedCompany] = useState<CompanyOutput>();
  const [selectedYear, setSelectedYear] = useState<string>(initialYear);
  const [currentFact, setCurrentFact] = useState<string>();
  const [currentFactShuffleKey, setCurrentFactShuffleKey] = useState<number>();
  const [nextFactShuffleKey, setNextFactShuffleKey] = useState<number>();
  const [companyIsLoading, setCompanyIsLoading] = useState<boolean>(true);
  const [emissionIsLoading, setEmissionIsLoading] = useState<boolean>(true);
  const [factIsLoading, setFactIsLoading] = useState<boolean>(true);
  const [formattedEmission, setFormattedEmission] = useState<string>();
  const [worstOffenders, setWorstOffenders] = useState<{
    [year: string]: number[];
  }>();

  useEffect(() => {
    const pulledWorstOffenders: {
      [year: string]: number[];
    } = {};
    Promise.all(
      _.map(availableYears, (year) =>
        api
          .apiCompaniesGet(
            1,
            40,
            undefined,
            _.parseInt(year),
            "fully_owned_emissions",
            _.parseInt(year)
          )
          .then(({ data: { companies } }) => _.map(companies, "id"))
      )
    ).then((companyIdArrays) => {
      setWorstOffenders(_.fromPairs(_.zip(availableYears, companyIdArrays)));
    });
  }, []);

  const fetchWorstOffender = (year?: string) => {
    setCompanyIsLoading(true);
    const fetchYear = year || _.sample(availableYears);
    const fetchId = _.sample(_.get(worstOffenders, fetchYear!!));
    return fetchId
      ? api.apiCompaniesCompanyIdGet(fetchId).then(({ data }) => {
          setSelectedCompany(data);
          setSelectedYear(fetchYear!!);
          setCompanyIsLoading(false);
        })
      : Promise.reject();
  };

  useEffect(() => {
    fetchWorstOffender();
  }, [worstOffenders]);

  const emission = useMemo(
    () =>
      _.get(selectedCompany, [
        "emissions_by_year",
        selectedYear,
        "fully_owned_emissions",
      ]),
    [selectedCompany, selectedYear]
  );

  useEffect(() => {
    setEmissionIsLoading(true);
    if (emission !== undefined) {
      api
        .apiFormatQuantityGet(`${emission} t`)
        .then(({ data: { formatted_quantity } }) => {
          setFormattedEmission(formatted_quantity);
          setEmissionIsLoading(false);
        });
    }
  }, [emission]);

  const yearOptions = useMemo(
    () =>
      _.chain(selectedCompany?.emissions_by_year)
        .keys()
        .map((yearOption) => <option value={yearOption}>{yearOption}</option>)
        .value(),
    [selectedCompany]
  );

  const refreshFact = (increment = true) => {
    setFactIsLoading(true);
    const shuffleKey = increment ? nextFactShuffleKey : currentFactShuffleKey;
    api
      .apiEmissionComparisonFactGet(emission, shuffleKey)
      .then(({ data: { fact, current_shuffle_key, next_shuffle_key } }) => {
        setCurrentFact(fact);
        if (increment || nextFactShuffleKey === undefined) {
          setCurrentFactShuffleKey(current_shuffle_key);
          setNextFactShuffleKey(next_shuffle_key);
        }
        setFactIsLoading(false);
      });
  };

  useEffect(() => {
    if (emission !== undefined) {
      refreshFact(false);
    }
  }, [emission]);

  const renderTooltip = (props: any) => (
    <Tooltip id="card-tooltip" {...props}>
      Click to randomize
    </Tooltip>
  );

  const topCardLoading =
    companyIsLoading || emissionIsLoading || !selectedCompany;
  const bottomCardLoading = topCardLoading || factIsLoading;

  return (
    <div className="card-container">
      <OverlayTrigger
        placement="right"
        delay={{ show: 250, hide: 0 }}
        overlay={renderTooltip}
      >
        <Button
          className="text-card"
          disabled={topCardLoading}
          onClick={!topCardLoading ? () => fetchWorstOffender() : undefined}
          bsPrefix="no-css"
        >
          {!topCardLoading ? (
            <>
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
                {` reported emissions equivalent to at least ${formattedEmission} of CO`}
                <sub>{"2"}</sub>
                {"."}
              </span>
            </>
          ) : (
            <span className="spinner-container">
              <Spinner
                className="initializing-spinner"
                animation="border"
                role="status"
              />
            </span>
          )}
        </Button>
      </OverlayTrigger>
      <OverlayTrigger
        placement="right"
        delay={{ show: 250, hide: 0 }}
        overlay={renderTooltip}
      >
        <Button
          className="text-card"
          disabled={bottomCardLoading}
          onClick={!bottomCardLoading ? () => refreshFact() : undefined}
          bsPrefix="no-css"
        >
          {!bottomCardLoading ? (
            <>{currentFact}</>
          ) : (
            <span className="spinner-container">
              <Spinner
                className="initializing-spinner"
                animation="border"
                role="status"
              />
            </span>
          )}
        </Button>
      </OverlayTrigger>
    </div>
  );
};

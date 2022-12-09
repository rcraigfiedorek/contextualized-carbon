import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import Button from "react-bootstrap/Button";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Spinner from "react-bootstrap/Spinner";
import Tooltip from "react-bootstrap/Tooltip";
import { CompanyOutput } from "../api";
import { api } from "../config";

interface CompanyEmissionInfoProps {
  company?: CompanyOutput;
  year?: string;
  onCompanyClick: () => void;
}

export const CompanyEmissionInfo: React.FunctionComponent<
  CompanyEmissionInfoProps
> = ({ company, year, onCompanyClick }) => {
  const [fact, setFact] = useState<string>();
  const [currentFactShuffleKey, setCurrentFactShuffleKey] = useState<number>();
  const [nextFactShuffleKey, setNextFactShuffleKey] = useState<number>();
  const [emissionIsLoading, setEmissionIsLoading] = useState<boolean>(true);
  const [factIsLoading, setFactIsLoading] = useState<boolean>(true);
  const [formattedEmission, setFormattedEmission] = useState<string>();

  const emission = useMemo<number | undefined>(
    () =>
      year
        ? _.get(company, ["emissions_by_year", year, "fully_owned_emissions"])
        : undefined,
    [company, year]
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

  const refreshFact = (increment = true): Promise<void> => {
    if (emission === undefined) return Promise.resolve();
    setFactIsLoading(true);
    const shuffleKey = increment ? nextFactShuffleKey : currentFactShuffleKey;
    return api
      .apiEmissionComparisonFactGet(emission, shuffleKey, true)
      .then(({ data }) => {
        setFact(data.fact);
        if (increment || nextFactShuffleKey === undefined) {
          setCurrentFactShuffleKey(data.current_shuffle_key);
          setNextFactShuffleKey(data.next_shuffle_key);
        }
        setFactIsLoading(false);
      });
  };

  useEffect(() => {
    refreshFact(false);
  }, [emission]);

  const renderTooltip = (props: any) => (
    <Tooltip id="card-tooltip" {...props}>
      Click to randomize
    </Tooltip>
  );

  const topCardLoading = !company || !year || emissionIsLoading;
  const bottomCardLoading = topCardLoading || factIsLoading;

  const topCardBody = (
    <>
      {`In ${year}, facilities in the US owned by `}
      <b>{company?.name}</b>
      {" reported emissions equivalent to "}
      <b>{formattedEmission}</b>
      {" of CO"}
      <sub>{"2"}</sub>
      {"."}
    </>
  );
  const bottomCardBody = fact ? (
    <div dangerouslySetInnerHTML={{ __html: fact }} />
  ) : (
    <></>
  );

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
          onClick={!topCardLoading ? () => onCompanyClick() : undefined}
          bsPrefix="no-css"
        >
          {!topCardLoading ? (
            topCardBody
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
            bottomCardBody
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

import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import Tooltip from "react-bootstrap/Tooltip";
import { CompanyOutput } from "../api";
import { api } from "../config";
import { ButtonCard } from "./ButtonCard";

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

  const topCardLoading = !company || !year || emissionIsLoading;
  const bottomCardLoading = topCardLoading || factIsLoading;

  return (
    <div className="card-container">
      <ButtonCard
        isLoading={topCardLoading}
        tooltipText="Click to randomize"
        onClick={onCompanyClick}
      >
        <>
          {`In ${year}, facilities in the US owned by `}
          <b>{company?.name}</b>
          {" reported emissions equivalent to "}
          <b>{formattedEmission}</b>
          {" of CO"}
          <sub>{"2"}</sub>
          {"."}
        </>
      </ButtonCard>
      <ButtonCard
        isLoading={bottomCardLoading}
        tooltipText="Click to randomize"
        onClick={refreshFact}
      >
        {fact ? <div dangerouslySetInnerHTML={{ __html: fact }} /> : <></>}
      </ButtonCard>
    </div>
  );
};

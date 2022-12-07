import _ from "lodash";
import { useMemo } from "react";
import { CompanyOutput } from "../api";
import { api } from "../config";

export const useWorstOffender = (
  availableYears: string[]
): ((year?: string) => Promise<[CompanyOutput, string]>) => {
  const worstOffenderKeysPromise: Promise<{
    [year: string]: number[];
  }> = useMemo(
    () =>
      Promise.all(
        _.map(availableYears, (yr) =>
          api
            .apiCompaniesGet(
              1,
              40,
              undefined,
              _.parseInt(yr),
              "fully_owned_emissions",
              _.parseInt(yr)
            )
            .then(({ data: { companies } }) => _.map(companies, "id"))
        )
      ).then((companyIdArrays) =>
        _.fromPairs(_.zip(availableYears, companyIdArrays))
      ),
    [availableYears]
  );

  const getWorstOffender = (
    year?: string
  ): Promise<[CompanyOutput, string]> => {
    return worstOffenderKeysPromise.then((worstOffenderKeys) => {
      const fetchYear = year || _.sample(availableYears);
      const fetchId = _.sample(_.get(worstOffenderKeys, fetchYear!!));
      return api
        .apiCompaniesCompanyIdGet(fetchId!!)
        .then(({ data }) => [data, fetchYear!!]);
    });
  };

  return getWorstOffender;
};

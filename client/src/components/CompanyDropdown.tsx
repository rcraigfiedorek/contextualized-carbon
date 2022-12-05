import classNames from "classnames";
import _ from "lodash";
import React, { MutableRefObject, useRef, useState } from "react";
import { AsyncTypeahead } from "react-bootstrap-typeahead";
import { CompanyOutput } from "../api";
import { api } from "../config";

interface CompanyDropdownProps {
  yearFilter?: string;
  selectedCompany: CompanyOutput;
  setSelectedCompany: (companyOutput: CompanyOutput) => void;
  typeaheadClassNames?: string;
}

export const CompanyDropdown: React.FunctionComponent<CompanyDropdownProps> = ({
  yearFilter,
  selectedCompany,
  setSelectedCompany,
  typeaheadClassNames,
}) => {
  const ref = useRef(null) as MutableRefObject<any>;
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [options, setOptions] = useState<CompanyOutput[]>([]);

  const parsedYearFilter = yearFilter ? _.parseInt(yearFilter) : undefined;

  function handleSearch(query: string): Promise<void> {
    setIsLoading(true);

    return api
      .apiCompaniesGet(
        1,
        20,
        query || undefined,
        parsedYearFilter,
        "fully_owned_emissions",
        parsedYearFilter
      )
      .then(({ data: { companies } }) => setOptions(companies))
      .catch(console.log)
      .finally(() => setIsLoading(false));
  }

  return (
    <AsyncTypeahead
      ref={ref}
      className={classNames(typeaheadClassNames, "company-dropdown")}
      filterBy={() => true}
      id="async-example"
      isLoading={isLoading}
      labelKey="name"
      minLength={3}
      defaultSelected={[selectedCompany]}
      onSearch={handleSearch}
      onBlur={() => {
        ref.current!!.state.selected = [selectedCompany];
        ref.current!!.state.showMenu = false;
      }}
      placeholder="Type to search..."
      onChange={(selected) => {
        const newCompany = _.head(selected) as CompanyOutput;
        if (newCompany) {
          setSelectedCompany(newCompany);
        }
      }}
      options={options}
    />
  );
};

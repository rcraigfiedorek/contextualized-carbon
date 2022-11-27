import _ from "lodash";
import React, { useState } from "react";
import { AsyncTypeahead, Highlighter } from "react-bootstrap-typeahead";
import { CompanyOutput, DefaultApi } from "../api";

interface CompanyDropdownProps {
  yearFilter?: string;
  selectedCompany: CompanyOutput;
  setSelectedCompany: (companyOutput: CompanyOutput) => void;
}

export const CompanyDropdown: React.FunctionComponent<CompanyDropdownProps> = ({
  yearFilter,
  selectedCompany,
  setSelectedCompany,
}) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [options, setOptions] = useState<CompanyOutput[]>([]);

  const parsedYearFilter = yearFilter ? _.parseInt(yearFilter) : undefined;

  const handleSearch = (query: string) => {
    setIsLoading(true);

    return new DefaultApi()
      .apiCompaniesGet(
        1,
        20,
        query,
        parsedYearFilter,
        "fully_owned_emissions",
        parsedYearFilter
      )
      .then(({ data: { companies } }) => setOptions(companies))
      .catch(console.log)
      .finally(() => setIsLoading(false));
  };

  return (
    <AsyncTypeahead
      filterBy={() => true}
      id="async-example"
      isLoading={isLoading}
      labelKey="name"
      minLength={3}
      onSearch={handleSearch}
      onChange={(selected) =>
        setSelectedCompany((_.head(selected) as CompanyOutput) || null)
      }
      selected={[selectedCompany]}
      options={options}
      renderMenuItemChildren={(option, props) => (
        <Highlighter search={props.text}>
          {(option as CompanyOutput).name}
        </Highlighter>
      )}
    />
  );
};

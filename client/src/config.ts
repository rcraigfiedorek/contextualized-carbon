import { Configuration, CorporateEmissionFactsApi } from "./api";

const basePath = process.env.REACT_APP_API_PATH || window.location.origin;

const apiConfiguration = new Configuration({ basePath });
export const api = new CorporateEmissionFactsApi(apiConfiguration);

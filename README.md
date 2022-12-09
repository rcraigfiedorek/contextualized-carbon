# Corporate Emissions Facts

Web application and API built on a stack of [Flask](https://flask.palletsprojects.com/en/2.2.x/), [SQLAlchemy](https://www.sqlalchemy.org/), [PostgreSQL](https://www.postgresql.org/), [React](https://reactjs.org/), and [Nginx](https://www.nginx.com/). Deployed using [Github Action](https://github.com/features/actions) and [Docker Compose](https://docs.docker.com/compose/) to a [Google Compute Engine](https://cloud.google.com/compute) instance.

Currently hosted at [emissions.craigf.io](https://emissions.craigf.io).

## Sources and Citations

All emissions data was obtained through the EPA's [Envirofacts Data Service API](https://www.epa.gov/enviro/envirofacts-data-service-api). The emissions data presented by the application can be most quickly verified using the EPA's [GHG search tool](https://enviro.epa.gov/envirofacts/ghg/search).

For citations regarding emissions comparison facts (e.g., the conversion rate between CO<sub>2</sub>-equivalent emissions and Arctic sea ice melt) please read [SOURCES.md](SOURCES.md).

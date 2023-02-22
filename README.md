![](https://img.shields.io/badge/Build%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiesitftung%20Berlin-blue)

# CKAN Filter Webtool

This application can be used to query which datasets are available in the [Berlin Open Data Portal](https://daten.berlin.de). The tool was developed to specifically find geodata that have been published as Open Data but have not yet been included in the Berlin Spatial Data Infrastructure (in the Berlin Geodata Portal, [FIS broker](https://www.berlin.de/sen/sbw/stadtdaten/geoportal/)). To better assess the relevance and suitability of the datasets, the tool automatically derives information about availability (Berlin-wide, only in one district, in several districts), as well as an initial prioritization, from the metadata. By customizing the keyword search in the advanced settings, the dataset query can be further specified or expanded to find non-spatial data, for example.

## Background

The Berlin administration makes geodata available as open data via the [FIS Broker](https://www.berlin.de/sen/sbw/stadtdaten/geoportal/). In addition to data sets that are collected and managed, i.e. that spatially cover the entire city of Berlin, there are a large number of other geodata that are the decentralized responsibility of the districts. Thus, not only the main administrations are data suppliers, but also all district administrations that independently collect geodata for their district. 

The project for the integration of district geodata into the geodata infrastructure (GDI) of the state of Berlin, commissioned by the Senate Department for Urban Development and Housing, has taken on the task of sounding out corresponding needs for processing and developing routines to standardize geodata records of all districts and to simplify merging. 

## Deployment

To run this application we suggest using docker and running the container behind a reverse proxy using nginx. See the [gunicorn documentation](https://docs.gunicorn.org/en/latest/deploy.html) for further information.

You also can run it with docker compose from source. Make sure to change exposed port in docker-compose.yml form 3333 to 80 (http) or 443 (https).

```bash
docker-compose build  
docker-compose up
```

or you can run it directly with python.

```bash
cd path/to/xml-schema-validator-v2
pip install --user --requirement requirements.txt
gunicorn --workers 3 --bind="0.0.0.0:3333" --log-level=info app:app
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Lisa-Stubert"><img src="https://avatars.githubusercontent.com/u/61182572?v=4?s=64" width="64px;" alt=""/><br /><sub><b>Lisa-Stubert</b></sub></a><br /><a href="https://github.com/technologiestiftung/ckan-filter-webtool/commits?author=Lisa-Stubert" title="Code">:computer:</a> <a href="https://github.com/technologiestiftung/ckan-filter-webtool/commits?author=Lisa-Stubert" title="Documentation">:book:</a></td>
    <td align="center"><a href="https://github.com/ester-t-s"><img src="https://avatars.githubusercontent.com/u/91192024?v=4?s=64" width="64px;" alt=""/><br /><sub><b>ester-t-s</b></sub></a><br /><a title="Code">:computer:</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

ODIS is supported by the Senate Department for Economic Economics, Energy and Public Enterprises and Investitionsbank Berlin from the funds of the State of Berlin. The tool was developed as part of a project with the Senate Department for Urban Development, Building and Housing.

<table>
  <tr>
    <td>
      <a href="https://odis-berlin.de">
        <br />
        <br />
        <img width="200" src="https://logos.citylab-berlin.org/logo-odis-berlin.svg" />
      </a>
    </td>
    <td>
      Together with: <a href="https://citylab-berlin.org/en/start/">
        <br />
        <br />
        <img width="200" src="https://logos.citylab-berlin.org/logo-citylab-berlin.svg" />
      </a>
    </td>
    <td>
      A project by: <a href="https://www.technologiestiftung-berlin.de/en/">
        <br />
        <br />
        <img width="150" src="https://logos.citylab-berlin.org/logo-technologiestiftung-berlin-en.svg" />
      </a>
    </td>
    <td>
      Supported by: <a href="https://www.berlin.de/rbmskzl/en/">
        <br />
        <br />
        <img width="80" src="https://logos.citylab-berlin.org/logo-berlin-senweb-en.svg" />
      </a>
    </td>
  </tr>
</table>

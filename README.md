![](https://img.shields.io/badge/Build%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiesitftung%20Berlin-blue)

# CKAN Filter Webtool

wip

## Background

wip

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
    <td align="center"><a href="https://fabianmoronzirfas.me/"><img src="https://avatars.githubusercontent.com/u/315106?v=4?s=64" width="64px;" alt=""/><br /><sub><b>Fabian Morón Zirfas</b></sub></a><br /><a href="https://github.com/technologiestiftung/xml-schema-validator/commits?author=ff6347" title="Code">💻</a> <a href="https://github.com/technologiestiftung/xml-schema-validator/commits?author=ff6347" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/Lisa-Stubert"><img src="https://avatars.githubusercontent.com/u/61182572?v=4?s=64" width="64px;" alt=""/><br /><sub><b>Lisa-Stubert</b></sub></a><br /><a href="https://github.com/technologiestiftung/xml-schema-validator/commits?author=Lisa-Stubert" title="Code">💻</a> <a href="https://github.com/technologiestiftung/xml-schema-validator/commits?author=Lisa-Stubert" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/vogelino"><img src="https://avatars.githubusercontent.com/u/2759340?v=4?s=64" width="64px;" alt=""/><br /><sub><b>Lucas Vogel</b></sub></a><br /><a href="https://github.com/technologiestiftung/xml-schema-validator/commits?author=vogelino" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

wip

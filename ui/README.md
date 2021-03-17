# ui

## Project setup

```shell
yarn install
```

Modify the values in `.env.development` and `.env.production` accordingly ( `.env.development` is used with `yarn serve` and `.env.production` is used with `yarn build` ).

Use the following values:

Variable name        | Variable value
-------------------- | ----------------------------------------------------------------------------------------------------------------------
`VUE_APP_SERVER_URL` | The vaccine-reefer-mgr URL (e.g. `http://localhost:8080` or `/reefer-mgr` if run on the same port in a different path)

> **Note** If you plan on adding new values, note that their keys must be prefixed with `VUE_APP_`.

### Compiles and hot-reloads for development

```shell
yarn serve
```

and open [localhost:4200](http://localhost:4200)

### Compiles and minifies for production

```shell
yarn build
```

### Lints and fixes files

```shell
yarn lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

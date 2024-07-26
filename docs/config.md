# Configutation

This section describes how to configure `Nexis`.

## Configuration File

`Nexis` uses TOML files for configuration.
The configuration file load order is:

1. `~/.config/nexis/nexis.toml`
2. `$CWD/nexis.toml`
3. Path from `-C/--config` option (if provided)

### `nexis.toml`

This is the default configuration used by `Nexis`.

```toml
mode = "dev"

[network]
api_url = "http://localhost:3000"

[development.network]
api_url = "http://localhost:3000"
```

## Customizing Configuration

The following options are available for `Nexis`:

- `mode`: `dev` or `prod` (default: `dev`)
- `version`: The version of Nexis to use (defaults to the local `Nexis` version)
- `network.api_url`: The base URL of the Nexis API (default: `http://localhost:3000`)
- `development.network.api_url`: The base URL of the Nexis API in development mode
  (default: `http://localhost:3000`)

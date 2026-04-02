# Telnyx LiveKit Agent Examples

Example voice AI agents built with the [LiveKit Agent Framework](https://docs.livekit.io/agents) and deployed on [Telnyx](https://telnyx.com).

## Examples

| Example | Description |
|---------|-------------|
| [restaurant](./restaurant) | Voice ordering assistant for an Italian restaurant |

## Prerequisites

- Python ≥ 3.10
- [LiveKit CLI](https://docs.livekit.io/home/cli/) (`lk`) ≥ 2.16.0
- A [Telnyx account](https://portal.telnyx.com) with an API key

## Quick Start

1. Clone this repo:

   ```bash
   git clone https://github.com/team-telnyx/telnyx-livekit-agent-examples.git
   cd telnyx-livekit-agent-examples/restaurant
   ```

2. Configure your environment:

   ```bash
   export LIVEKIT_URL=https://<region>.livekit-telnyx.com
   export LIVEKIT_API_KEY=<your-api-key>
   export LIVEKIT_API_SECRET=<your-secret>
   ```

   Available regions:

   | Region | URL |
   |--------|-----|
   | New York | `nyc1.livekit-telnyx.com` |
   | San Francisco | `sfo3.livekit-telnyx.com` |
   | Atlanta | `atl1.livekit-telnyx.com` |
   | Sydney | `syd1.livekit-telnyx.com` |

3. Deploy:

   ```bash
   lk agent deploy . --url $LIVEKIT_URL
   ```

## Documentation

- [LiveKit on Telnyx Docs](https://developers.telnyx.com/docs/livekit)
- [LiveKit Agent Framework](https://docs.livekit.io/agents)
- [livekit-plugins-telnyx](https://github.com/team-telnyx/telnyx-livekit-plugin)

## License

MIT

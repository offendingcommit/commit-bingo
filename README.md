# Bingo

![GitHub release (latest by date)](https://img.shields.io/github/v/release/OffendingCommit/commit-bingo)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/OffendingCommit/commit-bingo/ci.yml)
![GitHub](https://img.shields.io/github/license/OffendingCommit/commit-bingo)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UCQCU2f9J06IEVCyFx1k4T1g)](https://youtube.com/@offendingcommit)
[![Twitch Status](https://img.shields.io/twitch/status/offendingcommit)](https://twitch.tv/offendingcommit)

A customizable bingo board generator built with NiceGUI and Python. Create interactive bingo games for your streams, meetings, or events!

![Bingo Board Screenshot](https://raw.githubusercontent.com/OffendingCommit/commit-bingo/main/static/screenshot.png)

## Features

- **Custom Phrases**: Supply your own list of phrases for unique bingo experiences
- **Shareable Boards**: Generate view-only links to share with your audience
- **Interactive UI**: Mark squares with a simple click
- **Stream Integration**: Perfect for Twitch and YouTube streamers
- **Responsive Design**: Works on desktop and mobile devices
- **Docker Support**: Easy deployment with Docker
- **Kubernetes Ready**: Helm charts included for Kubernetes deployment

## Installation

### Prerequisites

- Python 3.12 or higher
- Poetry (recommended for dependency management)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/OffendingCommit/commit-bingo.git
cd commit-bingo

# Run the setup script
./setup.sh
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/OffendingCommit/commit-bingo.git
cd commit-bingo

# Install dependencies with Poetry
poetry install

# Run the application
poetry run python main.py
```

### Docker Installation

```bash
# Build the Docker image
docker build -t bingo .

# Run the container
docker run -p 8080:8080 bingo
```

### Kubernetes Deployment

```bash
# Deploy using Helm
cd helm && ./package.sh
helm install bingo ./bingo
```

## Usage

1. Access the application at `http://localhost:8080`
2. Customize your bingo phrases in `phrases.txt` or through the UI
3. Share the view-only link with your audience
4. Mark squares as they occur during your stream or event

## Configuration

### Custom Phrases

Edit the `phrases.txt` file to add your own phrases, one per line. The application will randomly select from these phrases to generate boards.

### Environment Variables

- `PORT`: Set the port number (default: 8080)
- `HOST`: Set the host address (default: 0.0.0.0)
- `DEBUG`: Enable debug mode (default: False)

## Development

For detailed development instructions and code standards, see [CLAUDE.md](CLAUDE.md).

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest

# Run linters
poetry run flake8
poetry run black --check .
poetry run isort --check .

# Format code
poetry run black .
poetry run isort .
```

## About the Author

[Offending Commit](https://github.com/OffendingCommit) is a software engineer, streamer, and content creator focused on coding, technology, and programming best practices.

- **YouTube**: [Offending Commit](https://youtube.com/@offendingcommit) - Tutorials, coding sessions, and tech reviews
- **Twitch**: [offendingcommit](https://twitch.tv/offendingcommit) - Live coding streams and interactive programming sessions
- **GitHub**: [OffendingCommit](https://github.com/OffendingCommit) - Open source projects and contributions

Join the community to learn about software development, DevOps, and tooling in a fun and engaging environment!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using conventional commits (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [NiceGUI](https://github.com/zauberzeug/nicegui) for the UI framework
- All contributors and community members
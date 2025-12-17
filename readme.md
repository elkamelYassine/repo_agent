# Repository Agent

 AI-powered tool that generates documentation and unit tests for any GitHub repository using Google Gemini.

## Features

-  **Auto Documentation**: Generates README and project overview
-  **Auto Tests**: Creates unit tests with proper frameworks (pytest, Jest, JUnit, etc.)

## Quick Start

### Prerequisites

- Python 3.10+
- Git
- Google Gemini API key

### Installation

```bash

git clone <your-repo-url>
cd repo_agent

pip install -r requirements.txt

cp .env .env
# Edit .env and add your GEMINI_API_KEY
```

### Usage

Simply run:

```bash
python main.py
```

Then enter any GitHub repository URL when prompted. That's it!

## What It Generates

```
output_<repo_name>/
├── README.md              
├── PROJECT_OVERVIEW.md    
└── tests/
    └── test_generated.*   
```



## Configuration

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here    # Required
```

## Project Structure

```
repo_agent/
├── main.py              
├── config.py            
├── github_service.py    
├── ai_service.py        
├── repo_analyzer.py     
├── doc_generator.py     
└── test_generator.py    
```

## Supported Languages

-  Python (pytest)
-  JavaScript/TypeScript (Jest)
-  Java (JUnit)
-  Go (testing)
-  And more...

## How It Works

1. **Clone**: Downloads the repository
2. **Analyze**: Scans files and structure
3. **Generate**: Uses AI to create docs and tests
4. **Save**: Outputs to organized directory

## Troubleshooting

**"GEMINI_API_KEY is required"**
- Create `.env` file with your API key
- Get key from Google AI Studio


---

**Note**: Always review AI-generated content before production use.

# NetFig - Network Configlet Generator

A modern Python CLI tool for generating network device configurations using CSV data and Jinja2 templates.

## Features

- 🚀 Modern CLI interface with rich terminal output
- 📝 Generate individual configuration files per device
- 📊 CSV-based variable management
- 🎨 Jinja2 templating support
- 📁 Automatic output directory management
- 📋 Single-file output option with timestamp
- ✨ Progress tracking and error handling

## Requirements

```
python >= 3.7
rich >= 13.9.4
typer >= 0.15.1
pandas >= 2.2.3
Jinja2 >= 3.1.5
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/netfig.git
cd netfig
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python netfig.py <csv_file> <template_file>
```

### With Custom Output Directory

```bash
python netfig.py <csv_file> <template_file> --output <directory_name>
```

### Example

```bash
python netfig.py variables.csv templates/cisco_template.j2 --output my_configs
```

### Help

```bash
python netfig.py --help
```

## Directory Structure

```
netfig/
├── input/          # Place your CSV files here
├── templates/      # Store your Jinja2 templates
├── output/         # Generated configurations
├── utils/          # Utility functions
├── netfig.py       # Main application
└── requirements.txt
```

## CSV Format

Your CSV file should contain variables for your templates. The first column's values will be used as filenames for individual configurations.

Example `variables.csv`:
```csv
hostname,interface,ip_address,subnet_mask
ROUTER01,GigabitEthernet0/1,192.168.1.1,255.255.255.0
ROUTER02,GigabitEthernet0/1,192.168.1.2,255.255.255.0
```

## Template Format

Use standard Jinja2 template syntax. Variables from CSV columns can be referenced directly.

Example `cisco_template.j2`:
```jinja
hostname {{ hostname }}
!
interface {{ interface }}
 ip address {{ ip_address }} {{ subnet_mask }}
 no shutdown
!
```

## Output

The script generates:
1. Individual `.txt` files for each row in your CSV (named after the first column)
2. A timestamped single file containing all configurations


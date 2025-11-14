# -Monitoring-Tool-for-Webpage

This FastAPI-based application periodically checks the availability and response time of a target website and stores the results in a PostgreSQL database.  
It automatically performs a check every **60 seconds**, calculates uptime statistics, and provides several API endpoints for real-time monitoring.

---

## Features

- Automatic background check every 60 seconds  
- Data stored in PostgreSQL using SQLAlchemy ORM  
- API endpoints for latest records and statistics  
- Configurable target URL via `.env` file  
- Thread-safe in-memory counters for uptime calculation  

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kwrossait1102/Monitoring-Tool-for-Webpage.git
cd your-repo-name
```

### 2. Install dependencies

Before installing dependencies, you should have already installed **Python 3.10+** and **PostgreSQL** on your device. **Make sure PostgreSQL service is running before starting the application.**

To install all required packages, run the following command in the **root directory of the project**:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit the `.env` file in the project root directory:

```ini
# Target webpage for monitoring
TARGET_URL=https://www.uni-stuttgart.de

# PostgreSQL connection string, change **password** to your own password
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/monitor

# Optional debug flag
DEBUG=True
```

### 4. Set Up PostgreSQL Database

Before running the application, ensure PostgreSQL is properly set up:

#### 4.1 Find your PostgreSQL service name

**On Windows:**

```bash
# List all PostgreSQL services
sc query state= all | findstr postgresql
```

Common service names: `postgresql-x64-15`, `postgresql-x64-16`, `PostgreSQL`

**On Linux:**

```bash
# Check if PostgreSQL service exists and its status
systemctl list-units --type=service | grep postgres

# Or check specific version
systemctl status postgresql
systemctl status postgresql@15-main  # Ubuntu/Debian with version 15
systemctl status postgresql-15       # Red Hat/CentOS with version 15
```

Common service names: `postgresql`, `postgresql@15-main`, `postgresql-15`

**On Mac:**

```bash
# If installed via Homebrew
brew services list | grep postgresql

# Check if PostgreSQL is running
ps aux | grep postgres
```

Common service names: `postgresql`, `postgresql@15`, `postgresql@16`

#### 4.2 Start PostgreSQL Service

**On Windows:**

```bash
# Check if PostgreSQL is running (replace with your service name from step 4.1)
sc query postgresql-x64-15

# Start PostgreSQL service if not running
net start postgresql-x64-15
```

**On Linux:**

```bash
# Start PostgreSQL service
sudo systemctl start postgresql

# Verify it's running
sudo systemctl status postgresql
```

**On Mac with Homebrew:**

```bash
# Start PostgreSQL service
brew services start postgresql@15

# Or for the default version
brew services start postgresql
```

#### 4.3 Create Database

Connect to PostgreSQL and create the required database:

**Step 1: Connect to PostgreSQL**

```bash
# Connect to PostgreSQL (default user is 'postgres')
psql -U postgres -h localhost

# If prompted for password, enter the password you set during PostgreSQL installation
```

**Note:**

- On Linux/Mac, you might need to use: `sudo -u postgres psql`
- If you encounter "password authentication failed", you may need to reset your PostgreSQL password

**Step 2: Create the database**

```sql
-- In the PostgreSQL prompt, create the database
CREATE DATABASE monitor;

-- Verify the database was created
\l

-- Exit
\q
```

#### 4.4 Verify Connection

Test the database connection using the credentials from your `.env` file:

```bash
# Test connection to the monitor database
psql -U postgres -h localhost -d monitor

# If successful, you should see the PostgreSQL prompt
# Exit with \q
```

**If you encounter authentication errors:**

- Make sure the password in your `.env` file matches your PostgreSQL user password
- On Linux/Mac, try: `sudo -u postgres psql -d monitor`

## Running this application

Start the FastAPI server with uvicorn (Please run this command in the **root directory of the project**):

```bash
# Run the application locally on port 8000
python -m uvicorn app.main:app --reload --port 8000
```

- After startup, the application will automatically:
- Perform a website availability check every 60 seconds
- Store results in the database
- Provide access to monitoring data through several endpoints

## Running Test

A simple pytest is provided to check that the root API endpoint ("/") responds correctly:

```bash
# Run the test in the **root directory of the project**
pytest -q
```

## Example Output

**GET /**  

```json
{
  "url": "https://www.uni-stuttgart.de",
  "status_code": 200,
  "available": true,
  "latency_ms": 135.42,
  "ttfb_ms": 54.11,
  "response_size_bytes": 18903,
  "consecutive_failures": 0,
  "availability_pct_since_start": 100.0
}
```

## API endpoints

```markdown

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Perform a manual availability check |
| `/records` | GET | Retrieve recent check records from database |
| `/stats` | GET | View uptime and failure statistics |

```

## License

MIT License © 2025 Qianyu Bu

<!-- End of README -->

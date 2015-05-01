# iCorruptionHack
http://ethics.harvard.edu/event/ending-institutional-corruption-hackathon

# Getting Started

1. Create new database
```
createdb campaigncon
```

2. Edit `keys.example.json` to include database parameters and rename it to `keys.json`

3. Seed the database
```
python main.py reset
```

# Ingesting New Data

1. Download data
```
# Download
sh download.sh
# Ingest into database
python main.py ingest
```

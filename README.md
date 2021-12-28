## Architecture

### sqlite database

#### Table

- podcast
    - id
    - date
    - title
    - path

### dbcreator.py

    dbcreator.py <podcasts.db> <start_date> <podcasts_dir>

- Rm podcasts.db
- Create db and table
- Iterate on all mp3 in podcasts_dir, sorted by name, depth-first, create an entry in podcast table

### feedgen.py

    feedgen.py [--now <date>] <podcasts.rss> <podcasts.db> <podcasts_dir_base_url>

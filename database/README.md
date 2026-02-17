# Database Setup - AI Social Intelligence

This directory contains the database schema, setup scripts, and configuration for the AI Social Intelligence platform.

## Database Overview

The system uses **PostgreSQL** as the primary database with the following key features:

- **Multi-tenant architecture** with user isolation
- **Full-text search** capabilities
- **JSONB fields** for flexible data storage
- **Time-series analytics** data
- **Advanced indexing** for performance
- **Row Level Security** (optional, commented out)

## Schema Tables

### Core Tables
- `users` - User accounts and authentication
- `user_plans` - Subscription plans and features
- `social_posts` - Collected social media posts with AI analysis
- `analytics_data` - Aggregated daily metrics
- `reports` - Generated AI reports
- `notification_settings` - User notification preferences

### Key Features
- **Sentiment Analysis**: Stores sentiment scores and classifications
- **Topic Modeling**: JSONB storage for extracted topics and keywords
- **Engagement Metrics**: Likes, shares, comments, views tracking
- **Full-text Search**: PostgreSQL's built-in text search capabilities
- **Time-series Data**: Optimized for analytics queries

## Quick Start with Docker

1. **Start PostgreSQL and Redis**:
   ```bash
   cd database
   docker-compose up -d
   ```

2. **Verify containers are running**:
   ```bash
   docker-compose ps
   ```

3. **Initialize the schema** (automatic with Docker volume mount)

## Manual Setup

### Prerequisites
- PostgreSQL 13+ installed
- Python 3.8+ with psycopg2
- Database user with creation privileges

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_social_db
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=ai_social_db
```

### Setup Steps

1. **Create the database**:
   ```bash
   python setup_db.py --create-db
   ```

2. **Initialize schema**:
   ```bash
   python setup_db.py --init-schema
   ```

3. **Add sample data**:
   ```bash
   python setup_db.py --sample-data
   ```

4. **Do everything at once**:
   ```bash
   python setup_db.py --all
   ```

## Database Functions

The schema includes several PostgreSQL functions for advanced analytics:

### Sentiment Trend Analysis
```sql
SELECT * FROM calculate_sentiment_trend(1, 7); -- user_id, days
```

### Topic Frequency Analysis
```sql
SELECT * FROM get_topic_frequency(1, 30); -- user_id, days
```

## Indexes and Performance

### Key Indexes
- GIN indexes for full-text search
- B-tree indexes on frequently queried columns
- Composite indexes for user + date queries
- JSONB indexes for metadata queries

### Query Optimization
- Generated columns for search vectors
- Partitioning strategy for large datasets (future enhancement)
- Connection pooling recommendations

## Backup and Recovery

### Manual Backup
```bash
pg_dump ai_social_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore
```bash
psql ai_social_db < backup_file.sql
```

### Docker Backup
```bash
docker exec ai_social_db pg_dump -U postgres ai_social_db > backup.sql
```

## Migration Strategy

For schema changes, use Alembic (SQLAlchemy migrations):

```bash
# Generate migration
alembic revision --autogenerate -m "Add new feature"

# Apply migration
alembic upgrade head
```

## Monitoring and Maintenance

### Key Metrics to Monitor
- Table sizes and growth rates
- Query performance (slow queries)
- Index usage and bloat
- Connection pool utilization

### Maintenance Commands
```sql
-- Analyze tables for query planning
ANALYZE;

-- Vacuum for space reclamation
VACUUM;

-- Reindex if needed
REINDEX DATABASE ai_social_db;
```

## Security Considerations

### Row Level Security (RLS)
The schema includes commented RLS policies for multi-tenant isolation.

### Data Encryption
- Sensitive data is hashed (passwords)
- Consider encrypting sensitive fields at rest

### Access Control
- Principle of least privilege
- Separate database users for application and admin access

## Troubleshooting

### Common Issues

1. **Connection refused**
   - Check PostgreSQL is running: `pg_isready -h localhost -p 5432`
   - Verify connection string and credentials

2. **Permission denied**
   - Ensure database user has proper privileges
   - Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql-*.log`

3. **Schema initialization fails**
   - Check SQL syntax in `schemas/init.sql`
   - Verify PostgreSQL version compatibility

### Logs
```bash
# View PostgreSQL logs
docker-compose logs postgres

# View application logs
tail -f /var/log/ai_social/app.log
```

## Development

### Local Development Setup
1. Use Docker Compose for isolated development environment
2. Run migrations for schema changes
3. Use sample data for testing features

### Testing
```bash
# Run database tests
pytest tests/test_database.py -v

# Load test data
python setup_db.py --sample-data
```

## Production Deployment

### High Availability
- Use PostgreSQL streaming replication
- Implement connection pooling (PgBouncer)
- Set up automated backups

### Performance Tuning
- Adjust `shared_buffers`, `work_mem`, `maintenance_work_mem`
- Monitor and optimize slow queries
- Implement partitioning for large tables

### Monitoring
- Set up PostgreSQL monitoring (pg_stat_statements)
- Implement alerting for critical metrics
- Regular health checks and maintenance
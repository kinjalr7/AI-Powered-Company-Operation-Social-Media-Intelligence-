# Architecture Diagram - Single Source of Truth

## Before Refactoring (Multiple Sources)

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Endpoints                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  analytics.py              dashboard_data.py      reports.py     │
│  ├─ Raw SQL Query 1        ├─ Raw SQL Query 3     ├─ Raw SQL 5   │
│  ├─ Manual Aggregation 1   ├─ Manual Agg 3        ├─ Manual Agg 5│
│  ├─ Sentiment Calc 1       ├─ Sentiment Calc 3    └─ ...         │
│  └─ ...                    └─ ...                                │
│                                                                   │
│  social_data.py                                                  │
│  ├─ Raw SQL Query 2                                              │
│  ├─ Manual Aggregation 2                                         │
│  └─ ...                                                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ❌ REDUNDANT QUERIES
                    ❌ DUPLICATE LOGIC
                    ❌ INCONSISTENT DATA
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Database                                    │
├─────────────────────────────────────────────────────────────────┤
│  social_posts table                                              │
│  ├─ id, user_id, platform, content, posted_at                   │
│  ├─ likes, comments, shares, reach                              │
│  ├─ sentiment_score, sentiment_label, topics, summary           │
│  └─ ...                                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## After Refactoring (Single Source of Truth)

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Endpoints                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  analytics.py              dashboard_data.py      reports.py     │
│  ├─ get_sentiment_dist()   ├─ get_post_count()    ├─ get_recent  │
│  ├─ get_post_count()       ├─ get_sentiment_dist()│   _posts()   │
│  ├─ get_recent_posts()     ├─ get_platform_break()└─ ...         │
│  └─ ...                    └─ ...                                │
│                                                                   │
│  social_data.py                                                  │
│  ├─ get_post_count()                                             │
│  ├─ get_sentiment_dist()                                         │
│  └─ get_platform_break()                                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ✅ CENTRALIZED QUERIES
                    ✅ SHARED LOGIC
                    ✅ CONSISTENT DATA
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Query Service Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  query_service.py                                                │
│  ├─ get_post_count()                                             │
│  ├─ get_sentiment_distribution()                                 │
│  ├─ get_recent_posts()                                           │
│  ├─ get_platform_breakdown()                                     │
│  └─ get_sentiment_by_platform()                                  │
│                                                                   │
│  ✅ Single source of truth                                       │
│  ✅ All queries read from social_posts                           │
│  ✅ No redundant calculations                                    │
│  ✅ Consistent data across all endpoints                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Database                                    │
├─────────────────────────────────────────────────────────────────┤
│  social_posts table                                              │
│  ├─ id, user_id, platform, content, posted_at                   │
│  ├─ likes, comments, shares, reach                              │
│  ├─ sentiment_score, sentiment_label, topics, summary           │
│  └─ ...                                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Query Service Functions

```
┌──────────────────────────────────────────────────────────────────┐
│                    query_service.py                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ get_post_count(db, user_id, platform=None, days=None)      │ │
│  │ ├─ SELECT COUNT(*) FROM social_posts                       │ │
│  │ ├─ WHERE user_id = :user_id                                │ │
│  │ ├─ Optional: AND platform = :platform                      │ │
│  │ ├─ Optional: AND posted_at >= start_date                   │ │
│  │ └─ Returns: int                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ get_sentiment_distribution(db, user_id, ...)               │ │
│  │ ├─ SELECT sentiment_label, COUNT(*)                        │ │
│  │ ├─ FROM social_posts                                       │ │
│  │ ├─ WHERE user_id = :user_id AND sentiment_label IS NOT NULL
│  │ ├─ GROUP BY sentiment_label                                │ │
│  │ └─ Returns: {'positive': int, 'negative': int, ...}        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ get_recent_posts(db, user_id, limit=20, ...)               │ │
│  │ ├─ SELECT * FROM social_posts                              │ │
│  │ ├─ WHERE user_id = :user_id                                │ │
│  │ ├─ ORDER BY posted_at DESC                                 │ │
│  │ ├─ LIMIT :limit                                            │ │
│  │ └─ Returns: List[Dict] with all post fields                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ get_platform_breakdown(db, user_id, days=None)             │ │
│  │ ├─ SELECT platform, COUNT(*), SUM(likes), ...              │ │
│  │ ├─ FROM social_posts                                       │ │
│  │ ├─ WHERE user_id = :user_id                                │ │
│  │ ├─ GROUP BY platform                                       │ │
│  │ └─ Returns: Dict[platform] → Dict[metrics]                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ get_sentiment_by_platform(db, user_id, ...)                │ │
│  │ ├─ SELECT platform, sentiment_label, COUNT(*)              │ │
│  │ ├─ FROM social_posts                                       │ │
│  │ ├─ WHERE user_id = :user_id                                │ │
│  │ ├─ GROUP BY platform, sentiment_label                      │ │
│  │ └─ Returns: Dict[platform] → Dict[sentiment] → count       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Example: Dashboard

### Before (Multiple Queries)
```
User Request
    ↓
get_dashboard_data()
    ├─ Query 1: SELECT COUNT(*) FROM social_posts
    ├─ Query 2: SELECT platform, COUNT(*) FROM social_posts GROUP BY platform
    ├─ Query 3: SELECT sentiment, COUNT(*) FROM social_posts GROUP BY sentiment
    ├─ Query 4: SELECT * FROM social_posts ORDER BY posted_at DESC LIMIT 8
    ├─ Manual aggregation of likes, comments, shares
    ├─ Manual calculation of average sentiment
    ├─ Manual grouping by date for timeseries
    └─ Return response
    ↓
Response (with redundant calculations)
```

### After (Centralized Queries)
```
User Request
    ↓
get_dashboard_data()
    ├─ get_post_count() → total_posts
    ├─ get_sentiment_distribution() → sentiment_dist
    ├─ get_platform_breakdown() → platform_breakdown
    ├─ get_recent_posts() → recent_posts_data
    ├─ Aggregate results from query_service
    └─ Return response
    ↓
Response (with consistent, centralized data)
```

---

## Module Dependencies

### Before (Scattered Dependencies)
```
analytics.py ──┐
               ├─→ SocialPost model
               ├─→ Raw SQL queries
               └─→ Manual calculations

dashboard_data.py ──┐
                    ├─→ SocialPost model
                    ├─→ Raw SQL queries
                    └─→ Manual calculations

reports.py ──┐
             ├─→ SocialPost model
             ├─→ Raw SQL queries
             └─→ Manual calculations

social_data.py ──┐
                 ├─→ SocialPost model
                 ├─→ Raw SQL queries
                 └─→ Manual calculations
```

### After (Centralized Dependencies)
```
analytics.py ──┐
               ├─→ query_service.py ──┐
dashboard_data.py ──┤                 ├─→ SocialPost model
                    ├─→ query_service.py ──┤
reports.py ──┤                 ├─→ Database
             ├─→ query_service.py ──┤
social_data.py ──┐                 │
                 └─→ query_service.py ──┘
```

---

## Benefits Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                        BEFORE                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Maintainability:  ⭐⭐☆☆☆  (Scattered logic)                    │
│  Consistency:      ⭐⭐☆☆☆  (Multiple sources)                   │
│  Performance:      ⭐⭐⭐☆☆  (Redundant queries)                  │
│  Reliability:      ⭐⭐☆☆☆  (Duplicate calculations)             │
│  Code Quality:     ⭐⭐⭐☆☆  (High duplication)                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

                              ↓
                    REFACTORING APPLIED
                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                        AFTER                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Maintainability:  ⭐⭐⭐⭐⭐  (Centralized logic)                 │
│  Consistency:      ⭐⭐⭐⭐⭐  (Single source)                     │
│  Performance:      ⭐⭐⭐⭐☆  (Optimizable queries)               │
│  Reliability:      ⭐⭐⭐⭐⭐  (No duplicates)                     │
│  Code Quality:     ⭐⭐⭐⭐⭐  (Low duplication)                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary

✅ **Single Source of Truth Achieved**

- All queries centralized in `query_service.py`
- All modules use the same query functions
- No redundant calculations
- Consistent data across all endpoints
- Improved maintainability and reliability

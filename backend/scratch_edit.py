import re

file_path = 'd:\\team\\backend\\app\\api\\dashboard_data.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove _demo_dashboard_data
pattern1 = re.compile(r'def _demo_dashboard_data\(days: int\) -> dict\[str, Any\]:.*?async def _get_current_user_optional', re.DOTALL)
if pattern1.search(content):
    content = pattern1.sub('async def _get_current_user_optional', content)
    print('Removed _demo_dashboard_data')
else:
    print('Could not find _demo_dashboard_data')

# 2. Replace current_user_opt is None fallback
pattern2 = re.compile(r'if current_user_opt is None:\s*return _demo_dashboard_data\(days=days\)')
if pattern2.search(content):
    content = pattern2.sub('if current_user_opt is None:\n        return {"data": [], "message": "No data available. Add posts to begin."}', content)
    print('Replaced current_user_opt is None fallback')
else:
    print('Could not find current_user_opt is None fallback')

# 3. Replace len(posts) == 0 fallback
pattern3 = re.compile(r'if len\(posts\) == 0 and \(len\(accounts\) == 0 or current_user\.email == "demo@example\.com"\):\s*print\(f"DEBUG: No recent data for \{current_user\.email\}\. Falling back to demo dataset\."\)\s*return _demo_dashboard_data\(days=days\)')
if pattern3.search(content):
    content = pattern3.sub('if len(posts) == 0:\n            return {"data": [], "message": "No data available. Add posts to begin."}', content)
    print('Replaced len(posts) fallback')
else:
    print('Could not find len(posts) fallback')

# 4. Remove forced sentiment distribution
pattern4 = re.compile(r'\s*# Force identical sentiment distribution ratio for every platform\s*item\["sentiment"\] = \{\s*"positive": int\(item\["total_posts"\] \* 0\.7\),\s*"neutral": int\(item\["total_posts"\] \* 0\.2\),\s*"negative": item\["total_posts"\] - int\(item\["total_posts"\] \* 0\.7\) - int\(item\["total_posts"\] \* 0\.2\)\s*\}')
if pattern4.search(content):
    content = pattern4.sub('', content)
    print('Removed forced sentiment')
else:
    print('Could not find forced sentiment')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

#!/bin/bash

# Script to apply Web Application Firewall (WAF) rules to block SQL injection attempts
# This script requires superuser privileges to execute

# WAF rules directory
WAF_RULES_DIR="/etc/modsecurity/rules/"

# Create a new WAF rule to block common SQL injection patterns
cat <<EOL > $WAF_RULES_DIR/block_sql_injection.conf
SecRule REQUEST_URI "(?i:(\%27)|(\'))|(\%3D)|(=)|--|(%23|#)|(/\*)|(\*/)|(@@)|(char\()|(nchar\()|(varchar\()|(alter\s+table)|(create\s+table)|(delete\s+from)|(drop\s+table)|(insert\s+into)|(select\s+)|(union\s+select))" \
    "id:999999,deny,status:403,log,msg:'Blocking SQL Injection Attempt'"
EOL

# Reload the WAF configuration
sudo systemctl reload apache2

if [ $? -eq 0 ]; then
  echo "WAF rules applied successfully to block SQL injection attempts."
else
  echo "Failed to apply WAF rules." >&2
fi

exit 0

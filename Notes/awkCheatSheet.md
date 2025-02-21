
# 🗂️ AWK Cheat Sheet

```bash
awk 'pattern { action }' file
```

## 🔹 Common AWK Commands (20+ Examples)

| Command                                       | Description                                   |
|-----------------------------------------------|-----------------------------------------------|
| `awk '{print}' file`                          | Print all lines                               |
| `awk '{print $1}' file`                       | Print the first column                        |
| `awk '{print $1, $3}' file`                   | Print the 1st and 3rd columns                 |
| `awk 'NR==3' file`                            | Print the 3rd line                            |
| `awk 'NR>2 && NR<6' file`                     | Print lines 3 to 5                            |
| `awk '/pattern/' file`                        | Print lines matching `pattern`                |
| `awk '!/pattern/' file`                       | Print lines **NOT** matching `pattern`        |
| `awk '{if ($2 > 50) print $1, $2}' file`      | Print if 2nd column > 50                      |
| `awk 'BEGIN {FS=":"} {print $1}' file`        | Set `:` as field separator                    |
| `awk '{sum+=$1} END {print sum}' file`        | Sum of the first column                       |
| `awk 'BEGIN {OFS="-"} {print $1, $2}' file`   | Change output field separator to `-`          |
| `awk '{if (NF > 3) print $0}' file`           | Print lines with more than 3 fields           |
| `awk '{count++} END {print count}' file`      | Count total lines                             |
| `awk '{for (i=1; i<=NF; i++) print $i}' file` | Print each field in a new line                |
| `awk '/^Error/ {print $0}' file`              | Print lines starting with "Error"             |
| `awk '$1 ~ /^[0-9]+$/' file`                  | Print lines where 1st field is a number       |
| `awk '{gsub(/old/, "new"); print}' file`      | Replace `old` with `new` in all lines         |
| `awk 'length($0) > 20' file`                  | Print lines longer than 20 characters         |
| `awk '{print toupper($0)}' file`              | Convert text to uppercase                     |
| `awk '{print tolower($0)}' file`              | Convert text to lowercase                     |
| `awk '{print "Line:", NR, $0}' file`          | Add line numbers to output                    |
| `awk 'ORS="," {print $1}' file`               | Print 1st column separated by commas          |

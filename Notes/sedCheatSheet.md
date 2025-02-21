
# ⚙️ SED Cheat Sheet

```bash
sed 'command' file
```

## 🔸 Common SED Commands (20+ Examples)

| Command                                         | Description                                   |
|-------------------------------------------------|-----------------------------------------------|
| `sed 's/foo/bar/' file`                        | Replace first occurrence of `foo` with `bar`  |
| `sed 's/foo/bar/g' file`                       | Replace **all** occurrences of `foo` with `bar` |
| `sed '2d' file`                                | Delete the 2nd line                           |
| `sed '2,4d' file`                              | Delete lines from 2 to 4                      |
| `sed '/pattern/d' file`                        | Delete lines matching `pattern`               |
| `sed -n '3,5p' file`                           | Print lines 3 to 5                            |
| `sed -i 's/foo/bar/g' file`                    | In-place replace in the original file         |
| `sed 's/\(foo\)/[\1]/g' file`                 | Highlight `foo` with brackets                 |
| `sed 's/^[ \t]*//;s/[ \t]*$//' file`         | Trim leading & trailing whitespaces           |
| `sed 's/[0-9]//g' file`                        | Remove all digits from the file               |
| `sed 's/.*error.*/[ERROR FOUND]/g' file`       | Replace entire lines containing "error"       |
| `sed '/^$/d' file`                             | Delete empty lines                            |
| `sed 's/abc/xyz/1' file`                       | Replace only the first occurrence of `abc`    |
| `sed -n '/pattern/p' file`                     | Print lines that match `pattern`              |
| `sed '5a\New Line Here' file`                 | Add a new line after the 5th line             |
| `sed '3i\Insert This Above' file`             | Insert text above the 3rd line                |
| `sed 's/\(.*\)/[\1]/' file`                 | Wrap each line with square brackets           |
| `sed 's/^/START: /' file`                      | Add `START: ` at the beginning of each line   |
| `sed 's/$/ :END/' file`                        | Add `:END` at the end of each line            |
| `sed 's/\(.*\)/\U\1/' file`                | Convert text to uppercase                     |
| `sed 's/\(.*\)/\L\1/' file`                | Convert text to lowercase                     |
| `sed 's/foo/bar/2' file`                       | Replace the 2nd occurrence of `foo` per line  |

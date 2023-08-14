current_branch=$(git symbolic-ref --short HEAD 2>/dev/null)
mkdir IFS="_" read -ra parts <<< "$current_branch"
target_dir = "../{$current_branch}/Lesson_{$parts[1]}_Bryukhovskikh"
mkdir $target_dir
cp -r src/* $target_dir
find $target_dir -type d -name "__pycache__" -exec rm -r {} \;
zip -r ../{$current_branch}/Lesson_{$parts[1]}_Bryukhovskikh.zip $target_branch

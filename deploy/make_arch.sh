current_branch=$(git symbolic-ref --short HEAD 2>/dev/null)
IFS="_" read -ra parts <<< "$current_branch"
cd ../${current_branch}/
target_dir="Lesson_${parts[1]}_Bryukhovskikh"
mkdir $target_dir
cp -r ../gb_patterns/src/* $target_dir
find $target_dir -type d -name "__pycache__" -exec rm -r {} \;
zip -r ${target_dir}.zip $target_dir

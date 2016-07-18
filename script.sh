for f in *; do
    if [[ -d $f ]]; then
        if [ -e "$f/requirements.txt" ]; then
            pip install -r "$f/requirements.txt"
        fi
        if [ "$f" != "mycroft-core" ]; then
            for file in $f/test/*.py; do
                if [[ -e "$file" ]]; then
                    mkdir -p "mycroft-core/test/skills/$f"
                    cp $file "mycroft-core/test/skills/$f"
                fi
            done
            cp -r $f mycroft-core/mycroft/skills/$f
        fi
    fi
done

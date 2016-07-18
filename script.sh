for f in *; do
    if [[ -d $f ]]; then
        if [ -e "$f/requirements.txt" ]; then
            pip install -r "$f/requirements.txt"
        fi
        if [ "$f" != "mycroft-core" ]; then
            cp -r $f mycroft-core/mycroft/skills/$f
        fi
    fi
done
